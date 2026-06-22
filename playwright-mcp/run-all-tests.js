async (page) => {
  const baseUrl = "http://localhost:3000";
  const email = "YOUR_TEST_EMAIL";
  const password = "YOUR_TEST_PASSWORD";

  function randomDigits(n) {
    let s = "";
    for (let i = 0; i < n; i++) s += Math.floor(Math.random() * 10);
    return s;
  }

  function randomFirstName() {
    return `Mcp${randomDigits(4)}`;
  }

  function randomLastName() {
    return `User${randomDigits(3)}`;
  }

  function randomMobile() {
    return `${[9, 8, 7, 6][Math.floor(Math.random() * 4)]}${randomDigits(9)}`;
  }

  function randomPincode() {
    return randomDigits(6);
  }

  async function assert(condition, message) {
    if (!condition) throw new Error(message);
  }

  async function resetSession(pageRef) {
    await pageRef.context().clearCookies();
    await pageRef.goto(`${baseUrl}/login`, { waitUntil: "domcontentloaded" });
    await pageRef.evaluate(() => localStorage.clear());
  }

  async function runTest(name, fn) {
    await resetSession(page);
    try {
      await fn();
      return { name, status: "passed" };
    } catch (error) {
      return { name, status: "failed", error: error.message || String(error) };
    }
  }

  function modalInput(pageRef, label) {
    return pageRef
      .locator("div")
      .filter({ has: pageRef.getByRole("heading", { name: "Add Contact" }) })
      .locator("div.space-y-1")
      .filter({ hasText: label })
      .locator("input");
  }

  async function waitForContactsTable(pageRef) {
    await pageRef.locator(".animate-spin").waitFor({ state: "hidden", timeout: 20000 });
  }

  async function login(pageRef) {
    await pageRef.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
    await pageRef.locator("#email").fill(email);
    await pageRef.locator("#password").fill(password);
    await pageRef.getByRole("button", { name: "Sign In" }).click();
    await pageRef.waitForURL(`${baseUrl}/contacts`, { timeout: 20000 });
    await waitForContactsTable(pageRef);
  }

  const results = [];

  results.push(
    await runTest("LOGIN-POS-001 successful login", async () => {
      await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
      await page.locator("#email").fill(email);
      await page.locator("#password").fill(password);
      await page.getByRole("button", { name: "Sign In" }).click();
      await page.waitForURL(`${baseUrl}/contacts`, { timeout: 20000 });
      await assert(
        await page.getByRole("heading", { name: "Contacts" }).isVisible(),
        "Contacts heading not visible"
      );
    })
  );

  results.push(
    await runTest("LOGIN-POS-002 show password toggle", async () => {
      await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
      await page.locator("#password").fill("secret");
      await assert(
        (await page.locator("#password").getAttribute("type")) === "password",
        "Password should be hidden"
      );
      await page.locator("#password").locator("xpath=..").getByRole("button", { name: "Show" }).click();
      await assert(
        (await page.locator("#password").getAttribute("type")) === "text",
        "Password should be visible"
      );
    })
  );

  results.push(
    await runTest("LOGIN-POS-003 hide password toggle", async () => {
      await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
      await page.locator("#password").fill("secret");
      const passwordField = page.locator("#password").locator("xpath=..");
      await passwordField.getByRole("button", { name: "Show" }).click();
      await passwordField.getByRole("button", { name: "Hide" }).click();
      await assert(
        (await page.locator("#password").getAttribute("type")) === "password",
        "Password should be hidden again"
      );
    })
  );

  results.push(
    await runTest("LOGIN-POS-004 authenticated redirect from login", async () => {
      await login(page);
      await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
      await page.waitForURL(`${baseUrl}/contacts`, { timeout: 15000 });
    })
  );

  results.push(
    await runTest("LOGIN-NEG-001 invalid credentials error", async () => {
      await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
      await page.locator("#email").fill("invalid@example.com");
      await page.locator("#password").fill("WrongPassword123!");
      await page.getByRole("button", { name: "Sign In" }).click();
      await page.locator("p.text-red-600").waitFor({ state: "visible", timeout: 10000 });
      await assert(
        await page.locator("p.text-red-600").isVisible(),
        "Error message not shown"
      );
      await assert(page.url().includes("/login"), "Should remain on login page");
    })
  );

  results.push(
    await runTest("LOGIN-NEG-002 sign in disabled without email", async () => {
      await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
      await assert(
        await page.getByRole("button", { name: "Sign In" }).isDisabled(),
        "Sign In should be disabled"
      );
      await page.locator("#password").fill("password");
      await assert(
        await page.getByRole("button", { name: "Sign In" }).isDisabled(),
        "Sign In should stay disabled without email"
      );
    })
  );

  results.push(
    await runTest("LOGIN-NEG-003 sign in disabled without password", async () => {
      await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
      await page.locator("#email").fill("user@example.com");
      await assert(
        await page.getByRole("button", { name: "Sign In" }).isDisabled(),
        "Sign In should be disabled without password"
      );
    })
  );

  results.push(
    await runTest("LOGIN-NEG-004 unauthenticated contacts redirect", async () => {
      await page.goto(`${baseUrl}/contacts`, { waitUntil: "networkidle" });
      await page.waitForURL(`${baseUrl}/login`, { timeout: 15000 });
    })
  );

  results.push(
    await runTest("CONTACTS-POS-001 contacts page loads with table", async () => {
      await login(page);
      await assert(
        await page.getByRole("heading", { name: "Contacts" }).isVisible(),
        "Contacts heading missing"
      );
      for (const header of ["Name", "Email", "Phone", "Company", "Updated"]) {
        await assert(
          await page.getByRole("columnheader", { name: header }).isVisible(),
          `Missing column header: ${header}`
        );
      }
    })
  );

  results.push(
    await runTest("CONTACTS-POS-002 add contact with valid data", async () => {
      await login(page);
      const firstName = randomFirstName();
      const lastName = randomLastName();
      const fullName = `${firstName} ${lastName}`;
      await page.getByRole("button", { name: "Add Contact" }).click();
      await modalInput(page, "First name").fill(firstName);
      await modalInput(page, "Last name").fill(lastName);
      await modalInput(page, "Email").fill(`${firstName}@example.com`);
      await modalInput(page, "Phone").fill(randomMobile());
      await modalInput(page, "PIN code").fill(randomPincode());
      await page.getByRole("button", { name: "Save Contact" }).click();
      await assert(
        !(await page.getByRole("heading", { name: "Add Contact" }).isVisible()),
        "Modal should close"
      );
      await assert(
        await page.getByRole("cell", { name: fullName }).first().isVisible({
          timeout: 20000,
        }),
        `Contact ${fullName} not found in table`
      );
    })
  );

  results.push(
    await runTest("CONTACTS-POS-003 search filters existing contact", async () => {
      await login(page);
      const firstName = randomFirstName();
      const lastName = randomLastName();
      const fullName = `${firstName} ${lastName}`;
      await page.getByRole("button", { name: "Add Contact" }).click();
      await modalInput(page, "First name").fill(firstName);
      await modalInput(page, "Last name").fill(lastName);
      await modalInput(page, "Phone").fill(randomMobile());
      await modalInput(page, "PIN code").fill(randomPincode());
      await page.getByRole("button", { name: "Save Contact" }).click();
      await page.getByRole("cell", { name: fullName }).first().waitFor({
        timeout: 20000,
      });
      await page.getByPlaceholder("Search contacts…").fill(firstName);
      await page.waitForResponse(
        (r) => r.url().includes("/contact") && r.request().method() === "GET"
      );
      await assert(
        await page.getByRole("cell", { name: fullName }).first().isVisible({
          timeout: 15000,
        }),
        "Search did not return the contact"
      );
    })
  );

  results.push(
    await runTest("CONTACTS-POS-004 cancel add contact closes modal", async () => {
      await login(page);
      await page.getByRole("button", { name: "Add Contact" }).click();
      await modalInput(page, "First name").fill("Cancel");
      await modalInput(page, "Last name").fill("Test");
      await modalInput(page, "Phone").fill(randomMobile());
      await modalInput(page, "PIN code").fill(randomPincode());
      await page.getByRole("button", { name: "Cancel" }).click();
      await assert(
        !(await page.getByRole("heading", { name: "Add Contact" }).isVisible()),
        "Modal should be closed"
      );
    })
  );

  results.push(
    await runTest("CONTACTS-POS-005 add contact required fields only", async () => {
      await login(page);
      const firstName = randomFirstName();
      await page.getByRole("button", { name: "Add Contact" }).click();
      await modalInput(page, "First name").fill(firstName);
      await modalInput(page, "Phone").fill(randomMobile());
      await modalInput(page, "PIN code").fill(randomPincode());
      await page.getByRole("button", { name: "Save Contact" }).click();
      await assert(
        await page.getByRole("cell", { name: firstName }).first().isVisible({
          timeout: 20000,
        }),
        "Required-fields-only contact not in table"
      );
    })
  );

  results.push(
    await runTest("CONTACTS-NEG-001 search no matches empty state", async () => {
      await login(page);
      await page.getByPlaceholder("Search contacts…").fill("zzz-nonexistent-contact-99999");
      await page.waitForResponse(
        (r) => r.url().includes("/contact") && r.request().method() === "GET"
      );
      await assert(
        await page.getByText("No contacts found.").isVisible({ timeout: 15000 }),
        "Empty state not shown"
      );
    })
  );

  results.push(
    await runTest("CONTACTS-NEG-002 submit without first name keeps modal open", async () => {
      await login(page);
      await page.getByRole("button", { name: "Add Contact" }).click();
      await modalInput(page, "Phone").fill(randomMobile());
      await modalInput(page, "PIN code").fill(randomPincode());
      await page.getByRole("button", { name: "Save Contact" }).click();
      await assert(
        await page.getByRole("heading", { name: "Add Contact" }).isVisible(),
        "Modal should remain open"
      );
    })
  );

  const passed = results.filter((r) => r.status === "passed").length;
  const failed = results.filter((r) => r.status === "failed").length;

  return {
    summary: { total: results.length, passed, failed },
    results,
  };
}
