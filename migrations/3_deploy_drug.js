const BloodSupplyChain = artifacts.require("BloodSupplyChain");

module.exports = function (deployer) {
  deployer.deploy(BloodSupplyChain);
};
