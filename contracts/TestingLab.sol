// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// bloodtesting and eligibility
contract TestingLab {

    struct TestReport {
        bytes32 donorId;
        bool eligible;
        string remarks;
        uint timestamp;
    }

    mapping(bytes32 => TestReport) public testReports;

    event BloodTested(bytes32 donorId, bool eligible, string remarks);

    function testBlood(
        bytes32 donorId,
        bool eligible,
        string memory remarks
    ) public {
        testReports[donorId] = TestReport(
            donorId,
            eligible,
            remarks,
            block.timestamp
        );

        emit BloodTested(donorId, eligible, remarks);
    }

    function getTestResult(bytes32 donorId)
        public
        view
        returns (bool, string memory)
    {
        TestReport memory report = testReports[donorId];
        return (report.eligible, report.remarks);
    }
}
