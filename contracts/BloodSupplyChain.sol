// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BloodDonation {

    struct Donor {
        string name;
        string bloodGroup;
        bool approved;
        bool tested;
        bool eligible;
    }

    mapping(address => Donor) public donors;

    event DonorRequested(address donor);
    event LabTestCompleted(address donor, bool result);
    event BloodVerified(address donor);
    event DataSentToHealthAuthority(address donor);

    function registerDonor(string memory _name, string memory _bg) public {
        donors[msg.sender] = Donor(_name, _bg, false, false, false);
        emit DonorRequested(msg.sender);
    }

    function labTest(address _donor, bool _result) public {
        donors[_donor].tested = true;
        donors[_donor].eligible = _result;
        emit LabTestCompleted(_donor, _result);
    }

    function verifyBlood(address _donor) public {
        require(donors[_donor].eligible, "Not eligible");
        donors[_donor].approved = true;
        emit BloodVerified(_donor);
    }

    function sendToHealthAuthority(address _donor) public {
        require(donors[_donor].approved, "Not verified");
        emit DataSentToHealthAuthority(_donor);
    }

    mapping(string => bool) public approvedDonors;

    function approveDonor(string memory donor) public {
        approvedDonors[donor] = true;
    }

    function isApproved(string memory donor) public view returns(bool) {
        return approvedDonors[donor];
    }

}
