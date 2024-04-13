import React, { useEffect, useState } from "react";
import "./App.css";
import UserService from "./service/UserService";

import {
  Button,
  Card,
  IconButton,
  Input,
  Typography,
} from "@material-tailwind/react";

function TrashIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="grey"
      className="h-5 w-5"
    >
      <path
        fillRule="evenodd"
        d="M16.5 4.478v.227a48.816 48.816 0 013.878.512.75.75 0 11-.256 1.478l-.209-.035-1.005 13.07a3 3 0 01-2.991 2.77H8.084a3 3 0 01-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 01-.256-1.478A48.567 48.567 0 017.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 013.369 0c1.603.051 2.815 1.387 2.815 2.951zm-6.136-1.452a51.196 51.196 0 013.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 00-6 0v-.113c0-.794.609-1.428 1.364-1.452zm-.355 5.945a.75.75 0 10-1.5.058l.347 9a.75.75 0 101.499-.058l-.346-9zm5.48.058a.75.75 0 10-1.498-.058l-.347 9a.75.75 0 001.5.058l.345-9z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    UserService.getUsers()
      .then((response) => {
        setUsers(response); // Log the users state after setting it
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const TABLE_HEAD = ["Name", "Email", "Actions"];

  return (
    <div className="App">
      <Card className="w-4/5 mx-auto">
        <table className="w-full min-w-max table-auto text-left">
          <thead>
            <tr>
              {TABLE_HEAD.map((head) => (
                <th
                  key={head}
                  className="border-b border-blue-gray-100 bg-blue-gray-50 p-4"
                >
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="font-normal leading-none opacity-70"
                  >
                    {head}
                  </Typography>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td className="border-b border-blue-gray-100 p-4">
                  <Typography variant="small" color="blue-gray">
                    {user.name}
                  </Typography>
                </td>
                <td className="border-b border-blue-gray-100 p-4">
                  <Typography variant="small" color="blue-gray">
                    {user.email}
                  </Typography>
                </td>
                <td className="border-b border-blue-gray-100 p-4">
                  <IconButton
                    variant="text"
                    onClick={() => {
                      UserService.deleteUser(user.id).then(() => {
                        setUsers(users.filter((u) => u.id !== user.id));
                      });
                    }}
                  >
                    <TrashIcon />
                  </IconButton>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
      <Card className="w-4/5 mx-auto p-5">
        <h3>Create user</h3>
        <Input
          type="text"
          placeholder="Name"
          className="w-1/2 mt-2"
          onChange={(e) => {
            setName(e.target.value);
          }}
        />
        <Input
          type="text"
          placeholder="Email"
          className="w-1/2 mt-4"
          onChange={(e) => {
            setEmail(e.target.value);
          }}
        />
        <Button
          onClick={() => {
            UserService.postUser(name, email).then((response) => {
              setUsers([...users, response]);
            });
          }}
          className="w-1/4 mx-auto mt-6"
        >
          Upload
        </Button>
      </Card>
    </div>
  );
}

export default App;
