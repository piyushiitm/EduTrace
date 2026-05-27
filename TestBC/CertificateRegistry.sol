// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CertificateRegistry {

    struct Certificate {
        string student;
        string authority;
        string certificatename;
        string hash;
    }

    Certificate[] public certificates;

    function addCertificate(
        string memory _student,
        string memory _authority,
        string memory _certificatename,
        string memory _hash
    ) public {

        certificates.push(
            Certificate(
                _student,
                _authority,
                _certificatename,
                _hash
            )
        );
    }
}