# ha_deskpro_integration
Experimental HomeAssistant integration for the Cisco Deskpro (and possibly other RoomOS devices).
## SERIOUSLY, *DANGER*, WILL ROBINSON
This integration is still very _unstable_ and it is the first one I've ever tried to build. Although the device interactions are really simple (so far), I don't know what I don't know yet.

Witness the lack of any unit tests, for example.

I strongly advise that you _NOT_ install this.
This is _NOT_ ready for prime-time yet.

### Disclaimer
I have no relationship with Cisco. I just happen to have access to a Cisco Deskpro, and I would like to make use of its awesome sensor package in my home automation.

## Installation instructions
1. BACK UP YOUR SYSTEM. 
1. install [HACS](https://hacs.xyz/) first
1. in HACS, add a Custom Repository
    * for the URL, enter the URL for this repo
    * for type, choose `Integration`
1. select the `Cisco Deskpro` integration in HACS
    * choose `Download`
1. edit your `configuration.yaml` file to add the Deskpro (see below)
1. edit your `secrets.yaml` file as described below
1. restart HomeAssistant

### Configuring the Deskpro
In order to fetch status off your deskpro,
you'll need to create a user with `User` privileges.
I'm sure there's documentation on cisco's site on how to do this.  I'll link to it eventually, but if you don't know how to do this yet, this integration is probably not for you.

1. create a new user specifically for this.  Don't use the default `admin` user-- it's really easy to create new users.
1. give the new user a strong password, since only automation is going to use it.
1. UNCHECK the default option to require the user change their password on first login.
1. SAVE the credentials.  You'll need them in the next step.

### configuration.yaml
Add the following to your HomeAssistant's `configuration.yaml`:
```yaml
sensor:
  - platform: cisco_deskpro
    host: !secret deskpro_hostname
    username: !secret deskpro_user
    password: !secret deskpro_pass
```
### secrets.yaml
Next, add the appropriate secrets to your `secrets.yaml`.  Not doing that yet? See [secrets.yaml](https://www.home-assistant.io/docs/configuration/secrets/). 

## What does this do?
This integration provides the following `sensor` entities, which update about once a minute:
* `deskpro_humidity`: the relative humidity
* `deskpro_ambient_noise_level`: the level of background noise in the room estimated by the device in decibels.  TL;DR: this is how noisy the room is *on average*
* `deskpro_level_of_noise_in_the_room_now`: the 'current' noise level, in decibels. For a good time, scream at your deskpro and watch the number change.
* `deskpro_people_count`: how many people the unit can detect in the room using whatever algorithms you've enabled.
* `deskpro_temperature`: the temperature in the room, as measured by the device.

There is a phantom `unnamed device` sensor that the integration also creates, which is always `0`. This is part of the update process and you should leave it alone until I can get rid of it.

## Limitations
### Manual Configuration
(as described above) You must bust out the text editor to configure this bad boy.

### There can be only one
I am but a mere mortal and own but a single one of these expensive beasties. So the integration only supports a single Deskpro at present.

My guess is this won't be a problem for most HomeAssistant users.  

### Insecure TLS Validation
The Deskpro uses self-signed TLS certs, so validation is unreliable.  This means that a malicious entity could spoof your deskpro and provide incorrect sensor data to your HomeAssistant.

So don't use these sensors for anything an intruder would want to influence, ok?
At least for now...





