#!/usr/bin/env node

'use strict';

const util = require('util');
const fs = require('fs');
const readline = require('readline');
const google = require('googleapis');
const googleAuth = require('google-auth-library');
const HamiFireManager = require('./libs/HamiFireManager')

const readFile = util.promisify(fs.readFile);

function authorize(credentials) {
  return new Promise((resolve, reject) => {
    var clientSecret = credentials.installed.client_secret;
    var clientId = credentials.installed.client_id;
    var redirectUrl = credentials.installed.redirect_uris[0];
    var auth = new googleAuth();
    var oauth2Client = new auth.OAuth2(clientId, clientSecret, redirectUrl);
    readFile('credentials.json')
      // .catch(error => console.log(error))
      .catch(error => getNewToken(oauth2Client))
      .then(token => oauth2Client.credentials = JSON.parse(token))
      .then(() => resolve(oauth2Client));
  });
}

function getNewToken(oauth2Client) {
  return new Promise((resolve, reject) => {
    var authUrl = oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: ['https://www.googleapis.com/auth/drive.metadata.readonly'],
    });
    console.log('Authorize this app by visiting this url: ', authUrl);
    var rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    rl.question('Enter the code from that page here: ', function(code) {
      rl.close();
      oauth2Client.getToken(code, function(err, token) {
        if (err) {
          console.log('Error while trying to retrieve access token', err);
          reject(err);
        }
        // storeToken(token);
        resolve(token);
      });
    });
  });
}

readFile('client_secret.json')
  .catch(error => console.log(error))
  .then(file => authorize(JSON.parse(file)))
  .then(auth => new HamiFireManager(auth))
  .then(hfm => hfm.findHamiRoot());
