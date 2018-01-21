#!/usr/bin/env node

'use strict';

const util = require('util');
const fs = require('fs');
const googleAuth = require('google-auth-library');

const readFile = util.promisify(fs.readFile);

function authorize(credentials) {
  return new Promise((resolve, reject) => {
    var clientSecret = credentials.installed.client_secret;
    var clientId = credentials.installed.client_id;
    var redirectUrl = credentials.installed.redirect_uris[0];
    var auth = new googleAuth();
    var oauth2Client = new auth.OAuth2(clientId, clientSecret, redirectUrl);
    readFile('credentials.json')
      .catch(error => console.log(error))
      .then(token => console.log(JSON.parse(token)));
  });
}

readFile('client_secret.json')
  .catch(error => console.log(error))
  .then(file => authorize(JSON.parse(file)));

