# Sean Straus' Home Assistant Configuration <img src="https://avatars1.githubusercontent.com/u/7644023?s=460&u=385a7ff0525e0838f1e302474d6c8931fc6db189&v=4" width="100" height="100" align="right"> 
(Home Assistant Supervised, Ubuntu Server 18.04.1 LTS, 2011 Mac Mini)

Last update: June 2, 2020 (Hass v.107.7)

Hello there. This is an incomplete and probably out of date description of what I'm doing with home assistant, but hopefully it will be of some use for ideas and samples to someone. In some places here I try to link to specific places in the relevant code in the config files. I can't promise all of the highlighted code blocks will be the right ones. If the link looks like it's going to the wrong part of the file, it's because I updated the file without updating the link, just go look elsewhere in that file.

Some things that may be interesting to you from my config which are not so common or are unique from how much I've obsessed over them are the:

* 10 Zone [Apple Airtunes](https://www.home-assistant.io/integrations/itunes/) whole house audio deployment with playlist buttons
* The [tensorflow](https://www.tensorflow.org/) based human detection using [frigate](https://github.com/blakeblackshear/frigate) and a [Google coral USB stick](https://coral.ai/products/accelerator/) on my [hikvision cameras](https://www.hikvision.com/content/dam/hikvision/en/support/regional-materials/brazil/DS-2CD2620F-I(S)%20%20-%20customized%20for%20Cangacu%20City%20-%20Bidding%2004-2015.pdf)
* The 12 zone [Honeywell Evohome](https://www.home-assistant.io/integrations/evohome/) heating system which is heavily automated with a custom [python script](https://github.com/scstraus/home-assistant-config/blob/master/python_scripts/set_heat_weather_override.py) to manage temperature settings and schedules based on the weather and automations to turn down the heat when the windows are open
* [Paradox Alarm Integration](https://community.home-assistant.io/t/paradox-alarm-mqtt-hassio-addon/38569/260) integrated with the human detection and many notification scenarios

There are a lot of other little things that I've not seen anyone else do, but I don't want to clutter up the intro too much, so more easter eggs inside.

Click the header links to be taken to the relevant file.

## [Lovelace UI](https://github.com/scstraus/home-assistant-config/blob/master/ui-lovelace.yaml)

So the first thing you might notice is that I use [custom header](https://github.com/maykar/custom-header) to shrink down the header and change it's color. I also simplify some of the views for my family and kiosks by removing the sidebar. 

I use [custom sidebar](https://github.com/Villhellm/custom-sidebar) to also rearrange the icons on the panel to sort them more in the order of how often I use them. 

For [themes](https://github.com/scstraus/home-assistant-config/blob/master/themes.yaml), I am using customized versions of the [Google Light theme](https://github.com/JuanMTech/google_light_theme) and [Midnight theme](https://community.home-assistant.io/t/midnight-theme/28598) which switch automatically 30 minutes after the sun goes down and when the sun comes up to match when my cameras go into infrared mode based on [this automation](https://github.com/scstraus/home-assistant-config/blob/master/automations/other_automations.yaml#L585-L612). I've just noticed that what's in the repo is actually my old themes file and that the new ones that were installed by HACS and modified by me to make more consistent looks when switching from day to night are not being backed up to the repo right now. I will try to fix that. I will also try to get around to making screenshots of the night theme to put here.

## [Tab 1: Main Dashboard](lovelace/Tab1_Home.yaml)


So, tab 1 is basically the main information view of the system, and if you scroll down, has quick access to most of the functions and important data in a concise format. Much of this is expanded in other tabs, but kept here as well for easy access.

![](readme_images/Tab1_dashboard.png)

This view also comes in a [kiosk flavor which I use on my 8" Amazon Kindle Fire tablets around the house with a more fixed layout for that device](lovelace/Tab1a_Home_Kiosk.yaml) which I achieve with [custom:lovelace-layout-card](https://github.com/thomasloven/lovelace-layout-card). Mostly there's just some layout changes and some customizations around not using camera streams but rather just the 5-10 second refreshing cameras due to the lower resources on the kindle.

![](readme_images/Tablet%20View.jpg)
  
But one interesting thing I have on the tablets is that they will use [popup cards](https://github.com/thomasloven/hass-browser_mod#popup) from the [Browser Mod](https://github.com/thomasloven/hass-browser_mod) custom component to popup the camera feeds on the tablets if it sees someone outside while we are home. Mostly we use this for keeping an eye on the kids while they are outside. If we are not at home with the alarm on or asleep, we will get emergency notifications on our phone instead. You can see these in the automations.


I will describe the cards I have here in the order I use them in my config so you can find them in the config file linked above.

**[Popup Cards](https://github.com/thomasloven/hass-browser_mod#popup) from custom component [Browser Mod](https://github.com/thomasloven/hass-browser_mod):**
Some popups that happen when you tap specific things

- **[Weekly weather popup](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L11-L16)** for when you tap on the daily forecast card to give you weekly variant
- **[Location descriptions and ETA](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L18-L55)** if you click on the locations for family members. This is a human readable description of where the person is, and an estimate of when they will be home if they are heading home, or how long it would take them if they started now if they aren't home. This is the same thing Alexa will read out if I ask her when they will be home.
- **[For air purifiers shows their availability and status as well as room AQI.](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L57-L115)** I had to customize this because they were going unavailable quite frequently, so I made input selects and automations that would cache the desired state until they became available and then change the real ones. I also changed AQI to standard AQI measurement rather than than direct particle measurement.
- **[Car popup when you click on the car lock button](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L117-L135)**, it will let you lock (but not unlock) the car.

**[Entity Filter Cards](https://www.home-assistant.io/lovelace/entity-filter/):**
These are how I get important statuses on lots of things without creating a lot of clutter, as they pop up only when they have something to tell me. I fudged the states on some stuff for the screenshot so you could see more of them. The real view usually looks more like what I show on the tablet.

- **[Emergency Alert](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L149-L233)** Pops up when there's something seriously wrong like the smoke alarms are going off, electricity is out, there's flooding, or (usually not actually very urgent) there's a human being shown on one of the cameras.
- **[Low Battery](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L235-L261)** Does what you'd expect. Tells you when the battery is low on one of about currently 15 devices like phones or zwave devices. I have more to add like my TRV's on the radiators which will come with a future HGI-80 release.
- **[What's Happening Today](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L263-L324)** This is the main heads up display that will show most of the status you need at a glance. It's the only one of these cards that's usually open. it shows the following things:
  - If we have a package coming from one of 4 carriers (DHL, Czech post, DPD, or GLS) based on emails we recieve
  - If it's the day to take out the trash or composting based on the schedules for those
  - If it's a good day to bike to work based on a lot of different weather conditions
  - If doors and windows around the house are open
  - If the dishwasher or clothes washing machines have finished washing and have clean clothes/dishes waiting to be taken out (some of this is done by monitoring the power with zwave switches if that's interesting to you)
  - If any of the alarm zones are armed
  - If the car needs gas or charging of it's battery (it's a hybrid), or if it has any faults it's reporting
  - How many total active coronavirus cases there are and how many new ones there were yesterday and today
- **[Upcoming Holidays](https://github.com/scstraus/home-assistant-config/blob/master/lovelace/Tab1_Home.yaml#L326-L365)** Didn't get this one on the screenshot, but it looks at 2 ical calendars for Czech national holidays and my daughter's school calendar to show holidays that are coming up in the next week and counts down number of days until they come with [custom:secondary-info-row](https://github.com/custom-cards/secondaryinfo-entity-row) to make the second row showing the number of days.

**I'll just list the rest of the cards here as you can see what they do on the screenshot:**

- [custom:weather-card-chart](https://github.com/Yevgenium/lovelace-weather-card-chart)

  (love having the chart in my weather forecast)

- [custom:vertical-stack-in-card](https://github.com/ofekashery/vertical-stack-in-card)

  (just combines the other cards into one card)

- [custom:button-card](https://github.com/custom-cards/button-card)

  (labels for the air quality card and reminders card because the ones on the card didn't match my theme)

- [custom:air-visual-card](https://github.com/dnguyen800/Air-Visual-Card)

  (air quality)

- [glance card](https://www.home-assistant.io/lovelace/glance/)

  (to show location of family)

- [custom:mod-card](https://github.com/thomasloven/lovelace-card-mod#mod-card) from the [card-mod addon](https://github.com/thomasloven/lovelace-card-mod)

  (to report a size for vertical stack-ins (so far lovelace couldn't handle this properly, but it looks like this [might get fixed finally](https://github.com/home-assistant/frontend/issues/5321#event-3379916050)))

- [custom:calendar-card](https://github.com/ljmerza/calendar-card)

  (for the reminders view)

- [conditional card](https://www.home-assistant.io/lovelace/conditional/)

  (to take away the label on the reminders view when there are no calendar items. Very kludgey way to fix the wrong font on the calendar label.)

- [custom:state-switch](https://github.com/thomasloven/lovelace-state-switch) and [custom:mod-card](https://github.com/thomasloven/lovelace-card-mod#mod-card) from the [card-mod addon](https://github.com/thomasloven/lovelace-card-mod)

  (to decide whether to show the real time camera feeds or the non-real time ones (one frame every 5-10 seconds), depending on whether I'm home or not. The real time feeds are very sensitive to device and bandwith and won't update if the conditions aren't right, so I try only to show them when I'm on wifi on a device capable of showing them (not on my kindle tablets).)

- [picture glance cards](https://www.home-assistant.io/lovelace/picture-glance/)

  (for the camera streams)

- [custom:mini-media-player](https://github.com/kalkih/mini-media-player)

  (for playing music from my itunes library to one of ~10 airplay zones around the house, each of which also uses a mini media player card to give an on/off button and volume control for the zone)

- [custom:button-card](https://github.com/custom-cards/button-card)

  (for playlist selection of music and shuffle control)

- [entity filter card](https://www.home-assistant.io/lovelace/entity-filter/)

  (to show anything important that's happening with the car, or very little if nothing much is happening.)

- [entities card](https://www.home-assistant.io/lovelace/entities/) with my climate entities

  (to show temperature in each heating zone. You can tap it to adjust the heat or see a graph. Also showing my air purifiers where I again use the [custom:secondaryinfo-entity-row](https://github.com/custom-cards/secondaryinfo-entity-row) to show the air quality index)

- [custom:search-card](https://community.home-assistant.io/t/lovelace-a-simple-search-card/127180)

  (to search for entities not shown here. I mainly use it to get history graphs of entities that are used in verious sensors so that I don't have to go to the endless wait that is the history pane)


## [Tab 2: Music](lovelace/Tab2_Music.yaml)

To play music on 10 AirTunes zones with pushbuttons for playlists.

![](readme_images/Tab2_music.png)

For  this one I am using the standard [media control card](https://www.home-assistant.io/lovelace/media-control/) as I don't mind it taking up a bit more room on this tab and it has pretty pictures of what's playing. 

For a persistent master volume slider I've had to use a [custom:slider-entity-row](https://community.home-assistant.io/t/slider-entity-row-add-sliders-to-entities-cards/140452) so that you don't have to tap the media player to get to it.

The playlist buttons are [custom:button-card](https://github.com/custom-cards/button-card)

And the volume and on/off controls for the speakers are [custom:mini-media-player](https://github.com/kalkih/mini-media-player) just like I used in the first tab.

There's also a [group](https://www.home-assistant.io/integrations/group/) for when I want to turn on/off all the speakers.

## [Tab 3: Heat](lovelace/Tab3_Heat.yaml)

This is the in-depth heat control which allows me to see the heat graph for each room and set more of the settings like whether the rooms are running from the schedule that's programmed into evohome, or in override mode. 

Most of the interesting stuff about my heating happens in the heating automations and my custom python script for setting heat profiles based on weather. This tab is mainly for debugging the automated side of it.

![](readme_images/Tab3_heat.png)

I use [popup cards](https://github.com/thomasloven/hass-browser_mod#popup) from the custom component [browser_mod](https://github.com/thomasloven/hass-browser_mod) to ensure I get the standard [history-graph](https://www.home-assistant.io/lovelace/history-graph/) graph if you tap on the pretty [custom:mini-graph-card](https://github.com/kalkih/mini-graph-card). The history graph also shows the historical setpoint of the thermostat and some guess at when the TRV was open, but lacks the color coding and beauty of the mini graph card. So I use the mini graph card for a quick overview of where there might be issues and to keep things pretty, and then I click if I want to dig into the "why" of what's happening with the heating to see the uglier and more detailed view. Maybe someday I will see if I can consolidate it all onto one graph, but I'm not sure it's possible with the graph card.

What I'm using for most of the view is mostly just a bunch of [custom:vertical-stack-in-cards](https://github.com/ofekashery/vertical-stack-in-card) to stack the [custom:mini-graph-card](https://github.com/kalkih/mini-graph-card) for each room on top of a [custom:lovelace-mini-thermostat card](https://github.com/Devqon/lovelace-mini-thermostat) for each room. That gives you the temperature history of each room with nice color coding for hot and cold on top of the control to set it manually. Mini thermostat saves a lot of space over the normal thermostat card here. 

Way down at the bottom, you will see an entities card with some input-selects for special heating cases like when I'm working from home or when there's a fire in the fireplace. Others happen automatically through automation like when my daughter is home from school for the day. The input selects are the output from my [python script](https://github.com/scstraus/home-assistant-config/blob/master/python_scripts/set_heat_weather_override.py) which takes the heating off of the schedule and turns it down depending on the weather.

## [Tab 4: Cameras](lovelace/Tab4_Cameras.yaml)

This tab shows the feeds of my security cameras on top with graphs of motion detection followed by the snapshots of the last 10 people who have been found by the human detection powered by [frigate](https://github.com/blakeblackshear/frigate) and a [Google coral USB stick](https://coral.ai/products/accelerator/) and [history graphs](https://www.home-assistant.io/lovelace/history-graph/)  of when humans were spotted.

![](readme_images/Tab4_cameras.png)

So basically the camera views are just the [picture glance card](https://www.home-assistant.io/lovelace/picture-glance/) for showing the cameras and some [horizontal](https://www.home-assistant.io/lovelace/horizontal-stack/) and [vertical stacks](https://www.home-assistant.io/lovelace/vertical-stack/) to arrange them and [history graphs](https://www.home-assistant.io/lovelace/history-graph/) to show the history of motion.

Below that is the same structure except I am monitoring the snapshots from the human detection and the history graphs of when humans are detected. I have added the [custom:swipe-card](https://github.com/bramkragten/custom-ui/tree/master/swipe-card) so that I can swipe between the latest snapshot of people detected and the previous 10 snapshots that were captured before that.

## [Tab 5: Appliances](lovelace/Tab5_Appliances.yaml)

This is my newest tab and is still a work in progress. The goal is to have the full controls and info from all my appliances like my dishwashers, washers and dryers, and also my car in some pretty [picture elements cards](https://www.home-assistant.io/lovelace/picture-elements/). Time will tell if I ever get around to creating all those pretty picture elements cards as they are quite a bit of work. The air purifiers already had some nice ones that some [other folks had made](https://community.home-assistant.io/t/lovelace-xiaomi-air-purifier-card/72924/4) and I just had to update them a bit for the most recent versions of hass. 

![](readme_images/Tab5_Appliances.png)

So, these are some [picture elements cards](https://www.home-assistant.io/lovelace/picture-elements/) that I got from [here](https://community.home-assistant.io/t/lovelace-xiaomi-air-purifier-card/72924/4). Nothing else happening here.

## [Tab 6: Alarm](lovelace/Tab6_Alarm.yaml)

So, this tab is messy and ugly and I don't like it much, but it gets the job done. The main problem is that my alarm system publishes 3 alarm panels due to the way it's partitioned for home and away modes and they all show up here. 

At some point I will merge these all together into an [MQTT alarm panel](https://www.home-assistant.io/integrations/alarm_control_panel.mqtt/), but that is a big job and hard to test now that we all stay home all the time due to coronavirus. Someday..

Anyhow, the view shows the alarm panels and some history on doors and windows being opened and motion sensors tripped along with the times of the most recent activities spotted in the house. It also has some cards that pop up in real time when motion is detected around the house in case you wanted to see that in real time.

![](readme_images/Tab6_Alarm.png)

So, I'm using some of the same cards you've seen already with a couple new ones.

* [Entity Filter Cards](https://www.home-assistant.io/lovelace/entity-filter/):

  (For real time popup when doors or windows are open or movement is detected)
  
* [Alarm Panel Cards](https://www.home-assistant.io/lovelace/alarm-panel/)

  (To show the alarm panels for the different zones)
  
* [custom:home-feed-card](https://github.com/gadgetchnnel/lovelace-home-feed-card)

  (Shows the most recent events around the house for doors/windows and motion. Honestly I didn't think it could do this kind of a view but the developer, [Steven Rollanson](https://github.com/gadgetchnnel) showed me how to get it to show it like this and it works well. If you go into [this thread](https://community.home-assistant.io/t/lovelace-home-feed-card/103719/148?u=scstraus), you can see my conversation about it and other ways that were suggested that probably work too but I haven't tried.)

* [history graphs](https://www.home-assistant.io/lovelace/history-graph/) 

  (to show the history of open doors and windows and when motion was detected)
  

## [Tab 7: Weather](lovelace/Tab7_Weather.yaml)

This one is just a collection of graphs and current weather data. I mostly use it for getting the idea of recent conditions for when I'm making automations, but sometimes I'm curious about the trend of one of these weather items and I take a peek over at this tab. 

![](readme_images/Tab7_weather.png)

These cards you've already seen elsewhere in my config.

- [custom:weather-card-chart](https://github.com/Yevgenium/lovelace-weather-card-chart)

  (love having the chart in my weather forecast)

- [custom:air-visual-card](https://github.com/dnguyen800/Air-Visual-Card)

  (air quality)

- [custom:button-card](https://github.com/custom-cards/button-card)

  (labels for the air quality card and reminders card because the ones on the card didn't match my theme)
  
- [entities card](https://www.home-assistant.io/lovelace/entities/) 

  (current weather data)
  
- [custom:mini-graph-card](https://github.com/kalkih/mini-graph-card)

  (historical weather data)

## [Tab 8: System](lovelace/Tab8_Tech.yaml)

Here is the system status of my Synology NAS that runs my Plex and Frigate instances as well as general backups and file serving and Home Assistant server (2011 Mac Mini + Ubuntu with RAID SSD's), as well as random other things I wanted shown somewhere for monitoring and tweaking.

![](readme_images/Tab8_System.png)

- [custom:vertical-stack-in-card](https://github.com/ofekashery/vertical-stack-in-card)

  (to merge everything for each server into a card)

- [custom:mini-graph-card](https://github.com/kalkih/mini-graph-card)

  (historical cpu, memory data and network data)

- [gauge card](https://www.home-assistant.io/lovelace/gauge/)

  (current battery levels and disk use)

- [entities card](https://www.home-assistant.io/lovelace/entities/) 

