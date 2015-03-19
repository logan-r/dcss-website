servers = $.get( "servers.json" );
servers.done(handleServerList);
servers.fail(failServerList);
navigator.geolocation.getCurrentPosition(knownPosition, unknownPosition);
