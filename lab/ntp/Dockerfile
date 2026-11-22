# Lab time server: chrony serving the clock of the Docker Desktop VM, which is the
# same clock the SIEM stamps events and alerts with. Lab only, not part of the SIEM.
FROM alpine:3.22
RUN apk add --no-cache chrony
COPY chrony.conf /etc/chrony/chrony.conf
EXPOSE 123/udp
# -d: foreground, -x: never adjust the system clock (the container cannot, and must not)
CMD ["chronyd", "-d", "-x", "-f", "/etc/chrony/chrony.conf"]
