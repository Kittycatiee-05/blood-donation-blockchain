const TestingLab = artifacts.require("TestingLab");

module.exports = function (deployer) {
  deployer.deploy(TestingLab);
};
