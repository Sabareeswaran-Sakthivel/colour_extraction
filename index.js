const express = require("express");
const multer = require("multer");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(
  cors({
    origin: "http://127.0.0.1:3001",
    methods: ["POST"],
  })
);

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads");
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const fileFilter = (req, file, cb) => {
  if (file.mimetype === "image/jpeg" || file.mimetype === "image/png") {
    cb(null, true);
  } else cb(null, false);
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: 1024 * 1024 * 5,
  },
});

app.use("/uploads/", express.static(__dirname + "/uploads"));

app.post("/api/pantones", upload.single("sample-image"), async (req, res) => {
  var spawn = require("child_process").spawn;
  var process = spawn("python3", ["./test.py"]);
  process.stdout.on("data", function (data) {
    res.send(data.toString());
  });
});

const PORT = 9000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}!`));
