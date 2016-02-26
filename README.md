# csh-automation

###Projector Controls
#####Projector Status
Query for the status of the Lounge projector. This will return the current power state, selected input, input sources and bulb hours.

```
GET https://control.csh.rit.edu/lounge/projector
```
Response:

```
{
  "projector": {
    "blank": false,
    "hours": 2145,
    "input": "HMDI 2",
    "power": false,
    "sources": {
      "Composite": null,
      "Computer1": "Aux VGA",
      "Computer2": null,
      "HDMI1": null,
      "HDMI2": "Receiver"
    }
  },
  "status": {
    "success": true
  }
}
```

#####Toggle Power
Example:

```
PUT https://control.csh.rit.edu/lounge/projector/power

{
  "token": {
    "id": ""
  },
  "power": {
	"state": true / false
  }
}
```
Response:

```
{
  "status": {
    "success": true
  }
}
```

#####Change Input
Example:

```
PUT https://control.csh.rit.edu/lounge/projector/input

{
  "token": {
    "id": ""
  },
  "input": {
	"select": [Item from sources list. Ex. "HDMI 2"]
  }
}
```
Response:

```
{
  "status": {
    "success": true
  }
}
```
#####Blank Projector
Example:

```
PUT https://control.csh.rit.edu/lounge/projector/blank

{
  "token": {
    "id": ""
  },
  "blank": {
	"state": true / false
  }
}
```
Response:

```
{
  "status": {
    "success": true
  }
}
```


###Receiver Controls
#####Receiver Status
Query for the status of the Lounge receiver. This will return the current power state, selected input, input sources and volume level.

```
GET https://control.csh.rit.edu/lounge/receiver
```
Response:

```
{
  "receiver": {
    "input": "HMDI 2",
    "mute": false,
    "sources": {
      "HDMI1": "Media PC",
      "HDMI2": "Aux HDMI",
      "HDMI3": "Chromecast",
      "HDMI4": "Raspberry Pi"
    },
    "volume": 46
  },
  "status": {
    "success": true
  }
}
```
#####Toggle Power
```
PUT https://control.csh.rit.edu/lounge/receiver/power

{
  "token": {
    "id": ""
  },
  "power": {
	"state": true / false
  }
}
```
Response:

```
{
  "status": {
    "success": true
  }
}
```
#####Change Input
```
PUT https://control.csh.rit.edu/lounge/receiver/input

{
  "token": {
    "id": ""
  },
  "input": {
	"select": [Item from sources list. Ex. "HDMI 2"]
  }
}
```
Response:

```
{
  "status": {
    "success": true
  }
}
```
#####Volume Adjustment
```
PUT https://control.csh.rit.edu/lounge/receiver/volume

{
  "token": {
    "id": ""
  },
  "volume": {
	"level": 1-127
  }
}
```
Response:

```
{
  "status": {
    "success": true
  }
}
```
#####Audio Mute Toggle
```
PUT https://control.csh.rit.edu/lounge/receiver/mute

{
  "token": {
    "id": ""
  },
  "mute": {
	"state": true / false
  }
}
```
Response:

```
{
  "status": {
    "success": true
  }
}
```
###Light Controls
#####Light Status
```
GET https://control.csh.rit.edu/lounge/lights
```
Response:

```
{
  "status": {
    "success": true
  },
  "lights": {
	"L1": true / false,
	"L2": true / false
  }
}
```
#####Toggle Lights
```
PUT https://control.csh.rit.edu/lounge/lights

{
  "token": {
    "id": ""
  },
  "lights": {
	"L1": true / false,
	"L2": true / false
	**You can update either an individual light or both simultaneously**
  }
}

```
Response:

```
{
  "status": {
    "success": true
  }
}
```
###Radiator Controls
#####Radiator Status
```
GET https://control.csh.rit.edu/lounge/radiator
```
Response:

```
{
  "status": {
    "success": true
  },
  "radiator": {
	"fan": true / false
  }
}
```
#####Toggle Radiator
```
PUT https://control.csh.rit.edu/lounge/lights

{
  "token": {
    "id": ""
  },
  "radiator": {
	"fan": true / false
  }
}

```
Response:

```
{
  "status": {
    "success": true
  }
}
```
