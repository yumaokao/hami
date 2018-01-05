#!/usr/bin/env node

'use strict';

const util = require('util');
const fs = require('fs');

const readFile = util.promisify(fs.readFile);

readFile('client_secret.json').then(file => authorize(JSON.parse(file)));

function authorize(credentials) {
  return new Promise((resolve, reject) => {
    var clientSecret = credentials.installed.client_secret;
    var clientId = credentials.installed.client_id;
    var redirectUrl = credentials.installed.redirect_uris[0];
    var auth = new googleAuth();
    var oauth2Client = new auth.OAuth2(clientId, clientSecret, redirectUrl);
    readFile('credentials.json')
      .then(token => console.log(JSON.parse(token)))
      .catch(error => console.log(error));
  });
};
