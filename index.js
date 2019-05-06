const express = require("express");
const app = express();
const logger = require("morgan");
const bodyParser = require("body-parser");
const ps = require("python-shell");

const apiRouter = express.Router();

app.use(logger("dev", {}));
app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true
  })
);

app.use("/api", apiRouter);

apiRouter.post("/sayHello", function(req, res) {
  const responseBody = {
    version: "2.0",
    template: {
      outputs: [
        {
          simpleText: {
            text: "hello I'm Ryan"
          }
        }
      ]
    }
  };

  res.status(200).send(responseBody);
});

app.listen(80, function() {
  console.log("listening on port 80");

  var options = {
    mode: "text",
    pythonPath: "",
    pythonOptions: ["-u"],
    scriptPath: "",
    args: [5, 3]
  };

  ps.PythonShell.run('getMeal.py', options, function(err, results) {
    console.log("results: %j", results);
  });
});
