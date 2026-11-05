#!/bin/bash
# Донастройка сервера, которую делал Claude Code в октябре 2026.
# Запускать от root на ВОССТАНОВЛЕННОМ сервере после того, как сайт уже поднят.
set -e

# 1. Swap 1 ГБ (на сервере было 1 ГБ RAM без swap, из-за чего MySQL убивался OOM).
if ! swapon --show | grep -q /swapfile; then
    fallocate -l 1G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
fi
# Сделать постоянным:
grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw,nofail 0 0' >> /etc/fstab

# 2. Ужать MySQL под маленькую память:
cp zz-lowmem.cnf /etc/mysql/mysql.conf.d/zz-lowmem.cnf
systemctl restart mysql
systemctl is-active mysql

echo "Готово. Свободная память:"
free -m | sed -n '2,3p'
