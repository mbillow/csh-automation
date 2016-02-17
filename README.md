# csh-automation

###Projector Controls
#####Projector Status
Query for the status of the Lounge projector. This will return the current power state, selected input, input sources and bulb hours.

```
GET https://control.csh.rit.edu/lounge/projector
```
Response:

```
status{
	"success": true
}
projector{
	"power": 0 (off) / 1 (on) / 2 (cooling),
	"input": "HDMI 2",
	"hours": 2145
	"sources": {
		"HDMI 1": null,
		"HDMI 2": "Mixer",
		"Computer 1": "Aux VGA",
		"Computer 2": null,
		"Composite": null
		},
	"blank": false,
}
```

#####Toggle Power
Example:

```
PUT https://control.csh.rit.edu/lounge/projector/power

token{
	"id": [shared_token]
}
power{
	"state": 0 (off) / 1 (on) 
}
```
Response:

```
status{
	"success": true
}
projector{
	"power": 1 (on) / 0 (cooling)
}
```

#####Change Input
Example:

```
PUT https://control.csh.rit.edu/lounge/projector/input

token{
	"id": [shared_token]
}
input{
	"select": [Item from sources list. Ex. "HDMI 2"]
}
```
Response:

```
status{
	"success": true
}
```
#####Blank Projector
Example:

```
PUT https://control.csh.rit.edu/lounge/projector/blank

token{
	"id": [shared_token]
}
```
Response:

```
status{
	"success": true
	"state": true [blanked] / false [video]
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
status{
	"success": true
}
receiver{
	"power": 0 (off) / 1 (on),
	"input": "HDMI 2",
	"volume": 69,
	"sources": {
		"HDMI 1": "Media PC",
		"HDMI 2": "Chromecast",
		"HDMI 3": "Aux HDMI",
		"HDMI 4": "Raspberry Pi"
		},
	"mute": false
}
```
#####Toggle Power
```
PUT https://control.csh.rit.edu/lounge/receiver/power

token{
	"id": [shared_token]
}
power{
    "state": 0 (off) / 1 (on) 
}
```
Response:

```
status{
	"success": true
}
```
#####Change Input
```
PUT https://control.csh.rit.edu/lounge/receiver/input

token{
	"id": [shared_token]
}
input{
    "select": [Item from sources list. Ex. "HDMI 2"]
}
```
Response:

```
status{
	"success": true
}
```
#####Audio Mute Toggle
```
PUT https://control.csh.rit.edu/lounge/receiver/mute

token{
	"id": [shared_token]
}
```
Response:

```
status{
	"success": true
	"state": 0 (umnuted) / 1 (muted)
}
```
###Light Controls
#####Light Status
```
GET https://control.csh.rit.edu/lounge/lights
```
Response:

```
status{
	"success": true
}
lights{
	"L1": 0 (off) / 1 (on),
	"L2": 0 (off) / 1 (on) 
}
```
#####Toggle Lights
```
PUT https://control.csh.rit.edu/lounge/lights

token{
	"id": [shared_token]
}
toggle{
	"L1": 0 (off) / 1 (on),
	"L2": 0 (off) / 1 (on) 
}
```
Response:

```
status{
	"success": true
}
```
