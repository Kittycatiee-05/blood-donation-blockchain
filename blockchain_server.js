const express = require("express");
const cors = require("cors");
const { ethers } = require("ethers");
const registryABI = require("./build/contracts/UserRegistry.json");

const app = express();
app.use(cors());
app.use(express.json());

// Ganache
const provider = new ethers.JsonRpcProvider("http://127.0.0.1:7545");

// Use ANY Ganache private key
const signer = new ethers.Wallet(
  "0xc5fa22c049ee960cce1599bf09d74713e9832dc30eeae7b88dfa975b9e4a4b7a",
  provider
);

// Truffle deployed address
const networkId = Object.keys(registryABI.networks)[0];
const contractAddress = registryABI.networks[networkId].address;

const contract = new ethers.Contract(
  contractAddress,
  registryABI.abi,
  signer
);

// REGISTER
app.post("/register", async (req, res) => {
  try {
    const { name, role, password } = req.body;
    const hash = ethers.keccak256(
      ethers.toUtf8Bytes(password)
    );

    const tx = await contract.registerUser(name, role, hash);
    await tx.wait();

    res.json({ success: true });
  } catch (e) {
    res.status(400).json({ error: e.reason || e.message });
  }
});

// LOGIN
app.post("/login", async (req, res) => {
  try {
    const { address, password } = req.body;
    const hash = ethers.keccak256(
      ethers.toUtf8Bytes(password)
    );

    const result = await contract.loginUser(address, hash);
    res.json({ success: result[0], role: result[1] });
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

app.listen(3000, () =>
  console.log("✅ Blockchain API running on port 3000")
);
