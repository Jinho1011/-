const express = require("express");
const app = express();
const logger = require("morgan");
const bodyParser = require("body-parser");
const { exec } = require("child_process");
const fs = require("fs");
const schedule = require("node-schedule");

const apiRouter = express.Router();

const mealObj = {
	today: {
		breakfast: "",
		lunch: "",
		dinner: ""
	},
	tommorow: {
		breakfast: "",
		lunch: "",
		dinner: ""
	}
};

app.use(logger("dev", {}));
app.use(bodyParser.json());
app.use(
	bodyParser.urlencoded({
		extended: true
	})
);

app.use("/api", apiRouter);

apiRouter.post("/meal/today", function(req, res) {
	const responseBody = {
		version: "2.0",
		data: {
			breakfast: mealObj.today.breakfast,
			lunch: mealObj.today.lunch,
			dinner: mealObj.today.dinner
		}
	};

	res.status(200).send(responseBody);
});

apiRouter.post("/meal/tommorow", function(req, res) {
	const responseBody = {
		version: "2.0",
		data: {
			breakfast: mealObj.tommorow.breakfast,
			lunch: mealObj.tommorow.lunch,
			dinner: mealObj.tommorow.dinner
		}
	};

	res.status(200).send(responseBody);
});

const execPy =  async () => {
	exec('python getMeal.py', function(err, stdout, stderr) {
		saveData()
	});
};

const saveData =  async () => {
	fs.readFile("today_meal.txt", "utf-8", (err, data) => {
		console.error(err);
		console.log("TCL: data", data);
		mealArr = data.split("|");
		mealObj.today.breakfast = mealArr[0];
		mealObj.today.lunch = mealArr[1];
		mealObj.today.dinner = mealArr[2];
	});

	fs.readFile("tommorow_meal.txt", "utf-8", (err, data) => {
		console.error(err);
		console.log("TCL: data", data);
		mealArr = data.split("|");
		mealObj.tommorow.breakfast = mealArr[0];
		mealObj.tommorow.lunch = mealArr[1];
		mealObj.tommorow.dinner = mealArr[2];
	});
}

var scheduler = schedule.scheduleJob("0 30 0 * * 1-7", function() {
	execPy()
});

app.listen(80, function() {
	console.log("listening on port 80");
	execPy()
});
