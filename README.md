Project is developed under another repo: https://github.com/mateuszbaranczyk/smart-home-api

This project allows control yeelight bulb from garmin watch (or any device that can send https requests).
Prepared for working with [HttpClient](https://apps.garmin.com/en-US/apps/da241207-e929-4cdf-9662-11ab17ffd70d).

It was created for fun to resolve use case and create infrastructure. 

Here is simple diagram how it works.

![Diagram](gl.drawio.png)


### TODO
- Detect devices
    - i can detect all devices in lan +
    - all of then will be saved in db +
    - i can call devvice by its name +

- Manage
    - list all devices +
    - set names by id +
    - endpoints auto setup +

- Endpoints 
    - one endpoint for function with device as arguent +

- Functions 
    - on/of +
    - timer
    - efects

- Tests
