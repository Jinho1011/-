const express = require("express");
const app = express();
const logger = require("morgan");
const bodyParser = require("body-parser");
const { exec } = require("child_process");
const fs = require("fs");

const apiRouter = express.Router();

const mealObj = {
	breakfast: "",
	lunch: "",
	dinner: ""
};

app.use(logger("dev", {}));
app.use(bodyParser.json());
app.use(
	bodyParser.urlencoded({
		extended: true
	})
);

app.use("/api", apiRouter);

apiRouter.post("/meal", function(req, res) {
	const responseBody = {
		version: "2.0",
		template: {
			outputs: [
				{
					meal: {
						breakfast: mealObj.breakfast,
						lunch: mealObj.lunch,
						dinner: mealObj.dinner
					}
				}
			]
		}
	};

	res.status(200).send(responseBody);
});

app.listen(80, function() {
	console.log("listening on port 80");

	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth() + 1;

	exec_query = `python getMeal.py ${mm} ${dd}`;

	exec(exec_query, function(err, stdout, stderr) {});

	fs.readFile("res_txt.txt", "utf-8", (err, data) => {
		console.log("TCL: data", data);
		mealArr = data.split(",");
		mealObj.breakfast = mealArr[0];
		mealObj.lunch = mealArr[1];
		mealObj.dinner = mealArr[2];
		console.log("TCL: mealObj", mealObj);
	});
});
