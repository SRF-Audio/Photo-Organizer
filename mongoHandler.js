const { MongoClient } = require("mongodb");

class MongoHandler {
  constructor(url) {
    this.url = url;
    this.client = new MongoClient(this.url, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    this.db = null;
  }

  // Connect to the database
  async connect(dbName) {
    try {
      await this.client.connect();
      this.db = this.client.db(dbName);
      console.log("Connected successfully to database");
    } catch (error) {
      console.error("Connection to MongoDB failed:", error);
    }
  }

  // Disconnect from the database
  async disconnect() {
    await this.client.close();
    console.log("Disconnected from database");
  }

  // Create a document in a specific collection
  async createDocument(collectionName, document) {
    try {
      const collection = this.db.collection(collectionName);
      const result = await collection.insertOne(document);
      console.log(`A document was inserted with the _id: ${result.insertedId}`);
      return result;
    } catch (error) {
      console.error("Create document failed:", error);
    }
  }

  // Read documents from a collection
  async readDocuments(collectionName, query = {}) {
    try {
      const collection = this.db.collection(collectionName);
      const documents = await collection.find(query).toArray();
      return documents;
    } catch (error) {
      console.error("Read documents failed:", error);
    }
  }

  // Update documents in a collection
  async updateDocuments(collectionName, filter, updateDoc) {
    try {
      const collection = this.db.collection(collectionName);
      const result = await collection.updateMany(filter, { $set: updateDoc });
      console.log(
        `${result.matchedCount} document(s) matched the filter, updated ${result.modifiedCount} document(s)`
      );
      return result;
    } catch (error) {
      console.error("Update documents failed:", error);
    }
  }

  // Delete documents from a collection
  async deleteDocuments(collectionName, query) {
    try {
      const collection = this.db.collection(collectionName);
      const result = await collection.deleteMany(query);
      console.log(`Deleted ${result.deletedCount} documents`);
      return result;
    } catch (error) {
      console.error("Delete documents failed:", error);
    }
  }
}

module.exports = MongoHandler;
