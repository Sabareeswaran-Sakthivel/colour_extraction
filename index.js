const cors = require("cors");
var express = require("express");
var multer = require("multer");
const fs = require("fs");

var app = express();
app.use(cors());

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./tmp");
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});
var upload = multer({ storage: storage });
// var multipleUpload = multer({storage: storage}).array('userPhoto',2);
// app.use(express.static(__dirname + '/public'));
app.use("/uploads", express.static("tmp"));

const BUZZER = 0;

app.post("/api/pantones", upload.single("image"), async (req, res) => {
  var spawn = require("child_process").spawn;
  var process = spawn("python3", ["./test.py", req.file.filename]);
  process.stdout.on("data", function (data) {
    res.send(data.toString());
  });
});

app.post("/api/photo", upload.array("image", 2), async (req, res) => {
  console.log("-=-=-=-=");
  console.log(req.files[0].filename);
  console.log(req.files[1].filename);
  var spawn = require("child_process").spawn;
  var process = spawn("python3", [
    "./test2.py",
    req.files[0].filename,
    req.files[1].filename,
  ]);
  // var process = spawn("python3", ["./test2.py"]);
  var filePath = "/uploads/mask.png";
  process.stdout.on("data", function (data) {
    //  res.send(data.toString());
    const payload = {};
    payload.data = fs.readFileSync(__dirname + filePath, "base64");
    res.send(payload);
  });
});

async function beforeImage() {
  var spawn = require("child_process").spawn;
  var process = spawn("python3", ["./crop.py"]);
  process.stdout.on("data", function (data) {
    var process = spawn("python3", ["./test4.py"]);
    process.stdout.on("data", function (data) {
      console.log(data.toString());
      // return "hello"
    });
  });
}

app.post("/api/pantones1", upload.array("image", 2), async (req, res) => {
  // console.log(req.files);
  console.log(req.files[0].filename);
  console.log(req.files[1].filename);
  var spawn = require("child_process").spawn;
  // var process = spawn("python3", ["./crop.py", req.files[0].filename]);
  // process.stdout.on("data", function (data) {
  //   var process = spawn("python3", ["./crop.py", req.files[1].filename]);
  //   process.stdout.on("data", function (data) {
  //     var filePath = "/uploads/mask.png";
  //     console.log("crop sone");
      var process = spawn("python3", [
        "./test2.py",
        req.files[0].filename,
        req.files[1].filename,
      ]);
      process.stdout.on("data", function (data) {
        //  res.send(data.toString());
        console.log(data);
        const payload = {};
        // payload.data = fs.readFileSync(__dirname + filePath, "base64");
        // console.log("---", data);
        res.send(data);
      });
    });
//   });
// });

app.post("/api/pantones2", upload.array("image", 2), async (req, res) => {
  console.log(req.files[0].filename);
  console.log(req.files[1].filename);
  var filePath = "/uploads/mask.png";
  var process = spawn("python3", [
    "./test2.py",
    req.files[0].filename,
    req.files[1].filename,
  ]);
  process.stdout.on("data", function (data) {
    //  res.send(data.toString());
    const payload = {};
    payload.data = fs.readFileSync(__dirname + filePath, "base64");
    console.log("---", data);
    res.send(payload);
  });
});

function getPalleteNumber() {
  var spawn = require("child_process").spawn;
  var process = spawn("python3", ["./test.py", req.file.filename]);
  let data;
  process.stdout.on("data", function (data) {
    data = data;
  });
}

const PORT = 8000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}!`));
