tsc
###

**tsc** (Test Case and Suite): Test artifacts used to validate use cases or verify requirements and specifications.

Each test case or suite must be documented using one of the formats below, depending on the traceability target:

**Use Case Validation Test**

.. code-block:: rst

    .. tsc:: TITLE
       :id: UNIQUE_ID
       :status: open
       :validation: USC_ID

       CONTENT_BODY

**Requirement Verification Test**

.. code-block:: rst

    .. tst:: TITLE
       :id: UNIQUE_ID
       :status: open
       :verify_req: REQ_ID

       CONTENT_BODY

**Specification Verification Test**

.. code-block:: rst

    .. tst:: TITLE
       :id: UNIQUE_ID
       :status: open
       :verify_spc: SPC_ID

       CONTENT_BODY

**Field Descriptions:**

- ``:id:``  
  A unique identifier for the test case. Must follow the regular expression pattern:  
  ``tst_demo_[0-9]{5,5}`` (e.g., `tst_demo_00001`).

- ``:status:``  
  Indicates the current lifecycle stage of the test.  
  Example values:  
  - ``open`` – the test is defined but not yet executed  
  - ``in-progress`` – the test is being developed or executed  
  - ``closed`` – the test is finalized and results are reviewed

- ``:validation:``  
  Use only for `tsc` entries. Refers to the ID of a use case (`usc`) that this test validates.

- ``:verify_req:``  
  Use only for `tst` entries. Refers to the ID of a requirement (`req`) that this test verifies.

- ``:verify_spc:``  
  Use only for `tst` entries. Refers to the ID of a specification (`spc`) that this test verifies.

- ``CONTENT_BODY``  
  Describes the purpose and content of the test. Should explain the setup, input, expected behavior, and verification method.

---

**Examples**

**Use Case Validation Test Example**

.. code-block:: rst

    .. tsc:: Login is validated with correct credentials
       :id: tst_demo_00001
       :status: open
       :validation: usc_demo_00001

       Simulates login with valid credentials. Checks successful redirection, token issuance, and session tracking.

**Requirement Verification Test Example**

.. code-block:: rst

    .. tst:: Password must include at least one special character
       :id: tst_demo_00002
       :status: open
       :verify_req: req_demo_00002

       Verifies system rejects password inputs lacking special characters, as required for security compliance.

**Specification Verification Test Example**

.. code-block:: rst

    .. tst:: Data encryption uses AES-256 as specified
       :id: tst_demo_00003
       :status: open
       :verify_spc: spc_demo_00001

       Confirms user data is encrypted with AES-256 before storage, meeting the design requirement in the encryption spec.
