# CAME Watchdog

Home Assistant custom integration to monitor ETI/Domo connection and automatically restart Home Assistant when connectivity is restored.

##  Features
- Detects ETI/Domo disconnection (`Server goes offline.`).
- Detects reconnection (`Successful authorization.`).
- Automatically triggers a safe restart of Home Assistant.

##  Installation

### Manual installation
1. Copy the folder `custom_components/came_watchdog` into your Home Assistant `custom_components` directory.

##  Configuration

1. Make sure that the logs from `custom_components.came.pycame.came_manager` are exposed at the `DEBUG` level.
   Add the following to your `configuration.yaml`:

   ```yaml
   logger:
     default: warning
     logs:
       custom_components.came.pycame.came_manager: debug
       
2. Add the following entry to your `configuration.yaml`:

   came_watchdog:
3. Restart Home Assistant.


##  Author
[@odoricof](https://github.com/odoricof)

