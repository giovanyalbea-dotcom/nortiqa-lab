rclone mount nortiqa-vps:/home/deploy Z: `
  --vfs-cache-mode writes `
  --vfs-cache-max-size 500M `
  --dir-cache-time 30s `
  --poll-interval 15s `
  --log-level ERROR `
  --volname "SC2027-VPS"
