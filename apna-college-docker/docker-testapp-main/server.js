const express = require("express");
const { MongoClient } = require("mongodb");

const app = express();
const PORT = process.env.PORT || 5050;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("public"));

const MONGO_URL =
  process.env.MONGO_URL ||
  "mongodb://admin:qwerty@mongo:27017/?authSource=admin";
const client = new MongoClient(MONGO_URL);

async function startServer() {
  await client.connect();
  console.log("Connected to MongoDB");

  const db = client.db("apnacollege-db");

  app.get("/getUsers", async (req, res) => {
    const data = await db.collection("users").find({}).toArray();
    res.send(data);
  });

  app.post("/addUser", async (req, res) => {
    await db.collection("users").insertOne(req.body);
    res.send("User inserted");
  });

  app.get("/health", (_req, res) => {
    res.send("OK");
  });

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
  });
}

startServer();