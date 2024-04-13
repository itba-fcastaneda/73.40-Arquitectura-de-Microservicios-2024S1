import axios from "axios";

const instance = axios.create({
  baseURL: process.env.API_URL || "http://localhost:8080",
});

class UserService {
  async getUsers() {
    try {
      const response = await instance.get("/users");
      console.log("Retrieved users:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error retrieving users:", error);
      throw error;
    }
  }

  async postUser(name, email) {
    try {
      const response = await instance.post("/users", { name, email });
      return response.data;
    } catch (error) {
      console.error("Error posting user:", error);
      throw error;
    }
  }

  async deleteUser(userId) {
    try {
      const response = await instance.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error("Error deleting user:", error);
      throw error;
    }
  }
}

export default new UserService();
