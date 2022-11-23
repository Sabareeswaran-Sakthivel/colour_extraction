
var express = require('express')
var multer  = require('multer')
var port = 3000;

var app = express()

var storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, './tmp')
    },
    filename: function (req, file, cb) {
      cb(null, file.originalname)
    }
})
var upload = multer({ storage: storage })
// app.use(express.static(__dirname + '/public'));
app.use('/uploads', express.static('tmp'));

// app.post('/profile-upload-single', upload.single('profile-file'), function (req, res, next) {
//   // req.file is the `profile-file` file
//   // req.body will hold the text fields, if there were any
//   console.log(JSON.stringify(req.file))
//   var response = '<a href="/">Home</a><br>'
//   response += "Files uploaded successfully.<br>"
//   // response += `<img src="${req.file.path}" /><br>`
//   return res.send(response)
// })
   

app.post("/api/pantones", upload.single("image"), async (req, res) => {
  var spawn = require("child_process").spawn;
  let fileName = req.file.originalname;
  console.log(req.file.originalname);
  var process = spawn("python3", ["./test.py"]);
  process.stdout.on("data", function (data) {
    res.send(data.toString());
  });
});

// app.get("/api/pantones", async(req, res) => {
//   res.send('Success');
// });

const PORT = 8000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}!`));
