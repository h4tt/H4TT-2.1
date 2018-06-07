const port = 3002;
const flag = 'flag{the-json-web-token-has-been-cracked!}'
const jwtSecret = 'flag';
// jwt : 2 sec
// flag : 32 sec
// secret : 40 min
// jwtflag : way to long

const express = require('express');
const app = express();
const server = app.listen(port);
const router = express.Router();
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');

app.use(bodyParser.json());

router.use((req, res, next)=>{
  next();
});

router.get('/get-endpoints', (req, res) => {
  res.json({
    endpoints: [
      {verb: 'GET', path: '/get-endpoints', description: 'Provides documentation on what end points are available and how to use them.'},
      {verb: 'GET', path: '/get-flag', description: 'Will return the flag, if you have the appropriate role.'},
      {verb: 'POST', path: '/login', description: 'Required to login before making other api requests. Uses Basic Auth. If no username or password is provided, a test user will be provided for you.'}
    ],
    'additional-info': 'Secured endpoints require Bearer Token Authentication; where the Authorization header has a value of: Bearer <token>\nexample: Authorization: Bearer eyJhbGciOi...'
  });
});

const ensureTokenHeaderFormat = (req, res, next) => {
  const bearerHeader = req.headers['authorization'];
  if(bearerHeader){
    const bearer = bearerHeader.split(' ');
    const bearerToken = bearer[1];
    req.token = bearerToken;
    next();
  }else{
    res.sendStatus(401);
  }
}
router.get('/get-flag', ensureTokenHeaderFormat, (req, res) => {
  jwt.verify(req.token, jwtSecret, (err, data) => {
    if(err){
      res.sendStatus(401);
    }else{
      console.log(data.user && data.user.role);
      if(data.user && data.user.role !== 'admin'){
        res.sendStatus(403);
      }else{
        res.json({flag});
      }
    }
  });
});

router.post('/login', (req, res)=>{
  console.log(req.body);
  const user = { id: 47, role: 'user' };
  const token = jwt.sign({ user }, jwtSecret);
  res.json({user, token});
});

app.use('/api', router);