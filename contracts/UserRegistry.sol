   // SPDX-License-Identifier: MIT

    // struct User {
    //     string name;
    //     string role;
    //     bool isRegistered;
    // }

    // mapping(address => User) public users;

    // event UserRegistered(address userAddress, string name, string role);

    // function registerUser(string memory name, string memory role) public {
    //     require(!users[msg.sender].isRegistered, "User already registered");

    //     users[msg.sender] = User({
    //         name: name,
    //         role: role,
    //         isRegistered: true
    //     });

pragma solidity ^0.8.0;

contract UserRegistry {

    struct User {
        bytes32 passwordHash;
        string role;
        bool exists;
    }
    mapping(string => User) private users;

    // function registerUser(
    //     string memory _username,
    //     string memory _password,
    //     string memory _role
    // ) public {
    //     require(!users[_username].exists, "User already exists");

    //     users[_username] = User(
    //         _username,
    //         _password,
    //         _role,
    //         true
    //     );
    // }

    function registerUser(
        string memory _username,
        string memory _password,
        string memory _role
    ) public {
        require(!users[_username].exists, "User already exists");
        bytes32 hash = keccak256(abi.encodePacked(_password));
        users[_username] = User({
            passwordHash: hash,
            role: _role,
            exists: true
            });
            }

    function loginUser(
        string memory _username,
        string memory _password
    ) public view returns (bool, string memory) {

        if (
            users[_username].passwordHash ==
            keccak256(bytes(_password))
        ) {
            return (true, users[_username].role);
        }

        return (false, "");
    }
}




