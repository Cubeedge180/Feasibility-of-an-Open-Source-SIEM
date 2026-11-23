#!/usr/bin/env bash
# Install the SIEM agent (Fluent Bit 5.1.3) on Debian/Kali, shipping auditd and auth.log.
#
#   sudo ./install.sh --ingest-host <mac-ip> --token <INGEST_TOKEN> [--ingest-port 8000]
#
# Needs internet for the packages. Re-running it updates the config and restarts the agent.
set -euo pipefail

FLUENT_BIT_VERSION=5.1.3
# Kali has no codename of its own in the Fluent Bit repo; it is Debian testing underneath.
FLUENT_BIT_CODENAME=${FLUENT_BIT_CODENAME:-bookworm}
CONF=/etc/fluent-bit/fluent-bit.conf
HERE=$(cd "$(dirname "$0")" && pwd)

ingest_host="" ingest_port=8000 token=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --ingest-host) ingest_host=$2; shift 2 ;;
    --ingest-port) ingest_port=$2; shift 2 ;;
    --token) token=$2; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[[ $EUID -eq 0 ]] || { echo "run as root (sudo)" >&2; exit 1; }
# Values go into the config file verbatim, so allow only safe characters.
[[ $ingest_host =~ ^[A-Za-z0-9.:-]+$ ]] || { echo "--ingest-host is required (IP or name)" >&2; exit 2; }
[[ $ingest_port =~ ^[0-9]{1,5}$ ]] || { echo "--ingest-port must be a number" >&2; exit 2; }
[[ $token =~ ^[A-Za-z0-9]{16,}$ ]] || { echo "--token must be 16+ letters/digits (openssl rand -hex 24)" >&2; exit 2; }
agent_host=$(hostname -s)
[[ $agent_host =~ ^[A-Za-z0-9.-]+$ ]] || { echo "unexpected hostname: $agent_host" >&2; exit 1; }

echo "== checking ingest at http://$ingest_host:$ingest_port/health"
curl -fsS --max-time 5 "http://$ingest_host:$ingest_port/health" || {
  echo "ingest not reachable: is 'docker compose up -d' running on the Mac?" >&2; exit 1; }
echo

echo "== packages: rsyslog (writes /var/log/auth.log), Fluent Bit $FLUENT_BIT_VERSION"
apt-get update -qq
apt-get install -y -qq rsyslog curl gpg
systemctl enable --now rsyslog
[[ -f /var/log/audit/audit.log ]] || { echo "no /var/log/audit/audit.log: install auditd first (W2)" >&2; exit 1; }

# The key comes over HTTPS from the vendor; apt then checks every package against it.
curl -fsSL https://packages.fluentbit.io/fluentbit.key | gpg --dearmor --yes -o /usr/share/keyrings/fluentbit-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/fluentbit-keyring.gpg] https://packages.fluentbit.io/debian/$FLUENT_BIT_CODENAME $FLUENT_BIT_CODENAME main" \
  > /etc/apt/sources.list.d/fluent-bit.list
apt-get update -qq
apt-get install -y -qq --allow-downgrades "fluent-bit=$FLUENT_BIT_VERSION"
apt-mark hold fluent-bit >/dev/null  # no silent upgrades between measured runs

echo "== config"
install -d -m 700 /var/lib/fluent-bit
umask 077
sed -e "s/@INGEST_HOST@/$ingest_host/" -e "s/@INGEST_PORT@/$ingest_port/" \
    -e "s/@INGEST_TOKEN@/$token/" -e "s/@AGENT_HOST@/$agent_host/" \
    "$HERE/fluent-bit.conf" > "$CONF"
chmod 600 "$CONF"
/opt/fluent-bit/bin/fluent-bit -c "$CONF" --dry-run

# Pin the unit to this config whatever the package's default file is.
install -d /etc/systemd/system/fluent-bit.service.d
cat > /etc/systemd/system/fluent-bit.service.d/siem.conf <<UNIT
[Service]
ExecStart=
ExecStart=/opt/fluent-bit/bin/fluent-bit -c $CONF
UNIT
systemctl daemon-reload
systemctl enable fluent-bit
systemctl restart fluent-bit
sleep 3
systemctl is-active --quiet fluent-bit || { journalctl -u fluent-bit -n 30 --no-pager; exit 1; }
echo "== done: $(/opt/fluent-bit/bin/fluent-bit --version | head -1) is shipping to $ingest_host:$ingest_port"
