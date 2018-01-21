#!/usr/bin/env node

'use strict';

const util = require('util');
const fs = require('fs');
const google = require('googleapis');
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
      .then(token => oauth2Client.credentials = JSON.parse(token))
      .then(() => resolve(oauth2Client));
  });
}

function listFiles(auth) {
  var service = google.drive('v3');
  service.files.list({
    auth: auth,
    pageSize: 10,
    fields: "nextPageToken, files(id, name)"
  }, function(err, response) {
    if (err) {
      console.log('The API returned an error: ' + err);
      return;
    }
    var files = response.files;
    if (files.length == 0) {
      console.log('No files found.');
    } else {
      console.log('Files:');
      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        console.log('%s (%s)', file.name, file.id);
      }
    }
  });
}

readFile('client_secret.json')
  .catch(error => console.log(error))
  .then(file => authorize(JSON.parse(file)))
  .then(auth => listFiles(auth));
