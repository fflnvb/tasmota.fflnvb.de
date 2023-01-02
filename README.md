# tasmota.fflnvb.de

## Environment Variables

| name                    | default               | description |
|:----                    |:--------              | -----------:|
| `VITE_APPLICATION_NAME` | `tasmota.fflnvb.de`   | Visible title on frontend
| `VITE_WIFI_MEDIUM`      | `60`                  | Wifi signal threshold to be passed for being rated medium
| `VITE_WIFI_BAD`         | `90`                  | Wifi signal threshold to be passed for being rated bad
| `BASE_IP`               | `192.168.1`           | Base IP for network scan
| `RANGE_FROM`            | `1`                   | Starting point for scan
| `RANGE_TO`              | `245`                 | End point for scan
| `TIMEOUT`               | `30`                  | Timeout for network requests in seconds
| `URL`                   | `/cm?cmnd=status%200` | Url that is being requested


## Installation

It is recommended to use `docker-compose` to run this package, as it simplifies updates and prevents conflicts with concurrent installations on the server.

```bash
git clone https://github.com/fflnvb/tasmota.fflnvb.de
cd tasmota.fflnvb.de
docker-compose build
docker-compose up
```

1. 

### Update

Instead of cloning the git project, simply do a `git pull` and get started


## Changelog

### 0.0.3 (2023-01-01)
- Added reloading
- Added spinner animation for first load
- Added updating last update indicator every second
- Changed communication between frontend and backend to WebSocket

### 0.0.2 (2022-12-24)
- Added creation date for json
- Added display of last update of json
- Added visualisation of signal strength, customizable via .env
- Added sort by column, ascending and descending
- Added asking for confirmation upon firmware upgrade
- Added search filter by topic
- Improved firmware version display (stripping off tasmota)
- Changed device listing as table 

### 0.0.1 (2022-12-23)
- Created first working prototype