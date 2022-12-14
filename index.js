const cors = require("cors");
var express = require("express");
var multer = require("multer");

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
// app.use(express.static(__dirname + '/public'));
app.use("/uploads", express.static("tmp"));


app.post("/api/pantones", upload.single("image"), async (req, res) => {
  var spawn = require("child_process").spawn;
  var process = spawn("python3", ["./test.py", req.file.filename]);
  process.stdout.on("data", function (data) {
   res.send(data.toString());
  });
});

app.get("/api/pantones", async (req, res) => {
  res.send("Success");
});

const PORT = 8000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}!`));
