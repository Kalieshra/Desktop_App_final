import { test, expect, Page } from "@playwright/test";
import path from "path";

const BASE_URL = "http://127.0.0.1:8000";
const CHANNEL_PK = 1;
const CHANNEL_DETAIL_URL = `${BASE_URL}/supplies/channel/${CHANNEL_PK}/`;
const TENDER_LIST_URL = `${BASE_URL}/supplies/tenders/`;
const TENDER_CREATE_URL = `${BASE_URL}/supplies/tender/add/?channel=${CHANNEL_PK}`;

const ATTACHMENT_FILE = path.join(
  __dirname,
  "artifacts",
  "test_attachment.txt",
);

// ── Page Object Model ─────────────────────────────────────────────────────────

class TenderFormPage {
  constructor(private page: Page) {}

  async gotoWithChannel(channelPk: number = CHANNEL_PK) {
    await this.page.goto(
      `${BASE_URL}/supplies/tender/add/?channel=${channelPk}`,
    );
    await this.page.waitForSelector('form[method="post"]');
  }

  async fillTenderName(value: string) {
    await this.page.locator("#id_tender_name").fill(value);
  }

  async checkFormalInspectionMinutes() {
    await this.page.locator("#id_formal_inspection_minutes").check();
  }

  async checkAdminFormationOrder() {
    await this.page.locator("#id_admin_formation_order").check();
  }

  async checkTechnicalMinutes() {
    await this.page.locator("#id_technical_minutes").check();
  }

  async checkMinutes1() {
    await this.page.locator("#id_minutes_1").check();
  }

  async checkTechnicalReport() {
    await this.page.locator("#id_technical_report").check();
  }

  async checkMinutes2() {
    await this.page.locator("#id_minutes_2").check();
  }

  async checkFinancialOpening() {
    await this.page.locator("#id_financial_opening").check();
  }

  async checkFinancialReport() {
    await this.page.locator("#id_financial_report").check();
  }

  async checkMinutes3() {
    await this.page.locator("#id_minutes_3").check();
  }

  async checkBidAcceptanceNotification() {
    await this.page.locator("#id_bid_acceptance_notification").check();
  }

  async uploadAttachment(filePath: string) {
    await this.page.locator("#id_attachment").setInputFiles(filePath);
  }

  async submit(): Promise<string> {
    await Promise.all([
      this.page.waitForNavigation({ waitUntil: "networkidle" }),
      this.page.locator('button[type="submit"]').click(),
    ]);
    return this.page.url();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: path.join(__dirname, "artifacts", `${name}.png`),
      fullPage: true,
    });
  }
}

class TenderListPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto(TENDER_LIST_URL);
    await this.page.waitForLoadState("networkidle");
  }

  async searchByName(query: string) {
    await this.page.locator('input[name="q"]').fill(query);
    await Promise.all([
      this.page.waitForNavigation({ waitUntil: "networkidle" }),
      this.page.locator('button[type="submit"]').click(),
    ]);
  }

  async filterByChannel(channelPk: number) {
    await this.page.locator('select[name="channel"]').selectOption(`${channelPk}`);
    await Promise.all([
      this.page.waitForNavigation({ waitUntil: "networkidle" }),
      this.page.locator('button[type="submit"]').click(),
    ]);
  }

  async getTenderRowByName(tenderName: string) {
    return this.page.locator("tr", { hasText: tenderName }).last();
  }

  async isTenderInList(tenderName: string): Promise<boolean> {
    const bodyText = await this.page.textContent("body");
    return (bodyText ?? "").includes(tenderName);
  }

  async getCheckIconCountForTender(tenderName: string): Promise<number> {
    const row = this.page.locator("tr", { hasText: tenderName }).last();
    const checkIcons = row.locator("i.bi-check-circle-fill");
    return await checkIcons.count();
  }

  async clickEditForTender(tenderName: string) {
    const row = this.page.locator("tr", { hasText: tenderName }).last();
    await row.locator('a[title="تعديل"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async clickDeleteForTender(tenderName: string) {
    const row = this.page.locator("tr", { hasText: tenderName }).last();
    await row.locator('a[title="حذف"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: path.join(__dirname, "artifacts", `${name}.png`),
      fullPage: true,
    });
  }
}

class ChannelDetailPage {
  constructor(private page: Page) {}

  async goto(pk: number = CHANNEL_PK) {
    await this.page.goto(`${BASE_URL}/supplies/channel/${pk}/`);
    await this.page.waitForLoadState("networkidle");
  }

  async clickAddTenderButton() {
    const btn = this.page.locator('a[href*="/supplies/tender/add/"]').first();
    await btn.click();
    await this.page.waitForLoadState("networkidle");
  }

  async isTendersTableVisible(): Promise<boolean> {
    // The tenders section has a header with المناقصات
    const header = this.page.locator("h6", { hasText: "المناقصات" });
    return await header.first().isVisible();
  }

  async getCheckIconCountForTender(tenderName: string): Promise<number> {
    const row = this.page.locator("tr", { hasText: tenderName }).last();
    const checkIcons = row.locator("i.bi-check-circle-fill");
    return await checkIcons.count();
  }

  async isTenderInTable(tenderName: string): Promise<boolean> {
    const tableText = await this.page
      .locator("table")
      .filter({ has: this.page.locator("th", { hasText: "اسم المناقصة" }) })
      .innerText()
      .catch(() => "");
    return tableText.includes(tenderName);
  }

  async clickEditForTender(tenderName: string) {
    // Navigate within the tenders table only
    const tendersTable = this.page.locator("table").filter({
      has: this.page.locator("th", { hasText: "اسم المناقصة" }),
    });
    const row = tendersTable.locator("tr", { hasText: tenderName }).last();
    await row.locator('a[title="تعديل"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async clickDeleteForTender(tenderName: string) {
    const tendersTable = this.page.locator("table").filter({
      has: this.page.locator("th", { hasText: "اسم المناقصة" }),
    });
    const row = tendersTable.locator("tr", { hasText: tenderName }).last();
    await row.locator('a[title="حذف"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: path.join(__dirname, "artifacts", `${name}.png`),
      fullPage: true,
    });
  }
}

// ── Helper: generate a unique tender name using timestamp ─────────────────────

function uniqueName(base: string): string {
  return `${base}-${Date.now()}`;
}

// ── Helper: create a tender via UI form ───────────────────────────────────────

interface TenderData {
  name: string;
  formalInspectionMinutes?: boolean;
  adminFormationOrder?: boolean;
  technicalMinutes?: boolean;
  minutes1?: boolean;
  technicalReport?: boolean;
  minutes2?: boolean;
  financialOpening?: boolean;
  financialReport?: boolean;
  minutes3?: boolean;
  bidAcceptanceNotification?: boolean;
  attachment?: string;
}

async function createTenderFromChannelUrl(
  page: Page,
  channelPk: number,
  data: TenderData,
): Promise<string> {
  const formPage = new TenderFormPage(page);
  await formPage.gotoWithChannel(channelPk);

  await formPage.fillTenderName(data.name);

  if (data.formalInspectionMinutes) await formPage.checkFormalInspectionMinutes();
  if (data.adminFormationOrder) await formPage.checkAdminFormationOrder();
  if (data.technicalMinutes) await formPage.checkTechnicalMinutes();
  if (data.minutes1) await formPage.checkMinutes1();
  if (data.technicalReport) await formPage.checkTechnicalReport();
  if (data.minutes2) await formPage.checkMinutes2();
  if (data.financialOpening) await formPage.checkFinancialOpening();
  if (data.financialReport) await formPage.checkFinancialReport();
  if (data.minutes3) await formPage.checkMinutes3();
  if (data.bidAcceptanceNotification) await formPage.checkBidAcceptanceNotification();
  if (data.attachment) await formPage.uploadAttachment(data.attachment);

  return await formPage.submit();
}

// ── Tests ─────────────────────────────────────────────────────────────────────

test.describe("Tenders Feature — Django Supplies App", () => {
  test.beforeEach(async ({ page }) => {
    // Verify server is responding and channel exists
    const response = await page.goto(CHANNEL_DETAIL_URL);
    expect(response?.status()).toBeLessThan(400);
  });

  // ── Scenario 1: Sidebar link ─────────────────────────────────────────────
  test("Scenario 1: Sidebar link المناقصات navigates to /supplies/tenders/", async ({
    page,
  }) => {
    await page.goto(`${BASE_URL}/supplies/`);
    await page.waitForLoadState("networkidle");

    // Locate the sidebar link by text
    const sidebarLink = page.locator("nav#sidebar a", {
      hasText: "المناقصات",
    });
    await expect(sidebarLink).toBeVisible();

    // Verify href
    const href = await sidebarLink.getAttribute("href");
    expect(href).toContain("/supplies/tenders/");

    // Click and verify navigation
    await sidebarLink.click();
    await page.waitForLoadState("networkidle");
    expect(page.url()).toContain("/supplies/tenders/");

    // Verify page heading
    await expect(page.locator("h3")).toContainText("المناقصات");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "t1_sidebar_nav.png"),
      fullPage: true,
    });
  });

  // ── Scenario 2: Create tender from list page ─────────────────────────────
  test("Scenario 2: Create a tender from /supplies/tenders/ page, verify it appears in list", async ({
    page,
  }) => {
    const tenderName = uniqueName("مناقصة-سيناريو2");

    // Navigate to the tenders list page
    const listPage = new TenderListPage(page);
    await listPage.goto();

    await listPage.takeScreenshot("t2_tender_list_before");

    // Verify the page heading and add button
    await expect(page.locator("h3")).toContainText("المناقصات");
    const addBtn = page.locator('a[href*="/supplies/tender/add/"]');
    await expect(addBtn).toBeVisible();

    // Click the إضافة مناقصة button (takes to form without channel pre-selected)
    await addBtn.click();
    await page.waitForLoadState("networkidle");
    expect(page.url()).toContain("/supplies/tender/add/");

    // The form without channel=?? requires us to select a channel from the hidden field
    // Instead, navigate directly with channel param so supply_channel is pre-filled
    const formPage = new TenderFormPage(page);
    await formPage.gotoWithChannel(CHANNEL_PK);

    await formPage.takeScreenshot("t2_empty_form");

    // Verify heading
    await expect(page.locator("h3")).toContainText("إضافة مناقصة جديدة");

    // Fill tender name and check some stages
    await formPage.fillTenderName(tenderName);
    await formPage.checkFormalInspectionMinutes();
    await formPage.checkTechnicalMinutes();
    await formPage.checkFinancialOpening();

    await formPage.takeScreenshot("t2_filled_form");

    const redirectUrl = await formPage.submit();

    // Should redirect to channel_detail after creation
    expect(redirectUrl).not.toContain("/tender/add/");
    expect(redirectUrl).toContain(`/channel/${CHANNEL_PK}/`);

    // Verify success message
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة المناقصة بنجاح");
    expect(bodyText).toContain(tenderName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "t2_after_create.png"),
      fullPage: true,
    });

    // Navigate to list page and verify tender appears
    await listPage.goto();
    const inList = await listPage.isTenderInList(tenderName);
    expect(inList).toBe(true);

    // Verify the checked stages show check icons (3 checked: formal_inspection_minutes, technical_minutes, financial_opening)
    const checkCount = await listPage.getCheckIconCountForTender(tenderName);
    console.log(`Scenario 2 — check icons in list: ${checkCount}`);
    expect(checkCount).toBe(3);

    await listPage.takeScreenshot("t2_tender_in_list");
  });

  // ── Scenario 3: Create tender from channel detail page button ────────────
  test("Scenario 3: Create tender from channel detail إضافة مناقصة button", async ({
    page,
  }) => {
    const tenderName = uniqueName("مناقصة-سيناريو3");

    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();

    // Verify the إضافة مناقصة button exists on channel detail
    const addTenderBtn = page.locator('a[href*="/supplies/tender/add/"]').first();
    await expect(addTenderBtn).toBeVisible();

    await channelPage.takeScreenshot("t3_channel_detail_before");

    // Click the button
    await addTenderBtn.click();
    await page.waitForLoadState("networkidle");

    // Should be on the tender create form with channel pre-set
    expect(page.url()).toContain("/supplies/tender/add/");
    expect(page.url()).toContain(`channel=${CHANNEL_PK}`);

    // Verify form heading
    await expect(page.locator("h3")).toContainText("إضافة مناقصة جديدة");

    // Fill the form
    const formPage = new TenderFormPage(page);
    await formPage.fillTenderName(tenderName);
    await formPage.checkAdminFormationOrder();
    await formPage.checkMinutes1();
    await formPage.checkMinutes2();
    await formPage.checkBidAcceptanceNotification();

    await formPage.takeScreenshot("t3_filled_form");

    const redirectUrl = await formPage.submit();

    // Should redirect to channel_detail
    expect(redirectUrl).toContain(`/channel/${CHANNEL_PK}/`);

    // Verify success message
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة المناقصة بنجاح");
    expect(bodyText).toContain(tenderName);

    await channelPage.takeScreenshot("t3_after_create");
  });

  // ── Scenario 4: Tenders table on channel detail shows checkmark icons ────
  test("Scenario 4: Channel detail tenders table shows ✓ icons for checked stages", async ({
    page,
  }) => {
    const tenderName = uniqueName("مناقصة-سيناريو4");

    // Create a tender with specific stages checked
    const redirectUrl = await createTenderFromChannelUrl(page, CHANNEL_PK, {
      name: tenderName,
      formalInspectionMinutes: true,
      technicalMinutes: true,
      technicalReport: true,
      financialOpening: true,
      financialReport: true,
    });

    expect(redirectUrl).toContain(`/channel/${CHANNEL_PK}/`);

    // Verify success and tender name visible
    const bodyAfterCreate = await page.textContent("body");
    expect(bodyAfterCreate).toContain("تم إضافة المناقصة بنجاح");
    expect(bodyAfterCreate).toContain(tenderName);

    // Navigate to channel detail and inspect tenders table
    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();

    await channelPage.takeScreenshot("t4_channel_detail_tenders");

    // The tenders section should be visible
    const tableVisible = await channelPage.isTendersTableVisible();
    expect(tableVisible).toBe(true);

    // The tender should be in the table
    const inTable = await channelPage.isTenderInTable(tenderName);
    expect(inTable).toBe(true);

    // Verify check icons: 5 stages were checked
    const checkCount = await channelPage.getCheckIconCountForTender(tenderName);
    console.log(`Scenario 4 — check icons in channel detail: ${checkCount}`);
    expect(checkCount).toBe(5);
  });

  // ── Scenario 5: Search filter on tender list page ────────────────────────
  test("Scenario 5: Search filter on /supplies/tenders/ narrows results", async ({
    page,
  }) => {
    const uniqueKeyword = `فريد-${Date.now()}`;
    const tenderName = `مناقصة-${uniqueKeyword}`;

    // Create a tender with unique name
    await createTenderFromChannelUrl(page, CHANNEL_PK, { name: tenderName });

    const listPage = new TenderListPage(page);
    await listPage.goto();

    // Search by unique keyword — should find it
    await listPage.searchByName(uniqueKeyword);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain(tenderName);

    await listPage.takeScreenshot("t5_search_results");

    // Search for something that won't match — should show empty state
    await listPage.searchByName("xxxx-no-match-xxxx");
    const emptyText = await page.textContent("body");
    expect(emptyText).toContain("لا توجد مناقصات بعد.");

    await listPage.takeScreenshot("t5_empty_search");
  });

  // ── Scenario 6: Channel filter on tender list page ───────────────────────
  test("Scenario 6: Channel filter on tender list page filters by channel", async ({
    page,
  }) => {
    const tenderName = uniqueName("مناقصة-سيناريو6");

    // Create a tender for channel 1
    await createTenderFromChannelUrl(page, CHANNEL_PK, { name: tenderName });

    const listPage = new TenderListPage(page);
    await listPage.goto();

    // Filter by channel PK — tender should appear
    await listPage.filterByChannel(CHANNEL_PK);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain(tenderName);

    await listPage.takeScreenshot("t6_channel_filter");
  });

  // ── Scenario 7: Edit tender and verify changes persist ───────────────────
  test("Scenario 7: Edit tender name and stage, verify changes persist in list", async ({
    page,
  }) => {
    const originalName = uniqueName("مناقصة-أصلية-سيناريو7");
    const updatedName = uniqueName("مناقصة-معدلة-سيناريو7");

    // Create the initial tender
    const afterCreateUrl = await createTenderFromChannelUrl(page, CHANNEL_PK, {
      name: originalName,
      formalInspectionMinutes: true,
    });
    expect(afterCreateUrl).toContain(`/channel/${CHANNEL_PK}/`);

    const bodyAfterCreate = await page.textContent("body");
    expect(bodyAfterCreate).toContain("تم إضافة المناقصة بنجاح");

    // Go to channel detail and click edit
    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();

    const inTableBefore = await channelPage.isTenderInTable(originalName);
    expect(inTableBefore).toBe(true);

    await channelPage.takeScreenshot("t7_before_edit");

    // Click edit for this specific tender
    await channelPage.clickEditForTender(originalName);

    // Should be on the edit form
    await expect(page.locator("h3")).toContainText("تعديل مناقصة");

    // Change the tender name
    const nameInput = page.locator("#id_tender_name");
    await nameInput.clear();
    await nameInput.fill(updatedName);

    // Also check an additional stage (admin_formation_order)
    await page.locator("#id_admin_formation_order").check();

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "t7_edit_form.png"),
      fullPage: true,
    });

    // Submit the edit form
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('button[type="submit"]').click(),
    ]);

    // Verify success message and updated name
    const bodyAfterEdit = await page.textContent("body");
    expect(bodyAfterEdit).toContain("تم تعديل المناقصة بنجاح");
    expect(bodyAfterEdit).toContain(updatedName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "t7_after_edit.png"),
      fullPage: true,
    });

    // Verify original name is no longer in channel detail tenders table
    const inTableAfterEdit = await channelPage.isTenderInTable(originalName);
    expect(inTableAfterEdit).toBe(false);

    // Verify updated name is present
    const updatedInTable = await channelPage.isTenderInTable(updatedName);
    expect(updatedInTable).toBe(true);

    // Verify 2 check icons (formalInspectionMinutes + adminFormationOrder both checked)
    const checkCount = await channelPage.getCheckIconCountForTender(updatedName);
    console.log(`Scenario 7 — check icons after edit: ${checkCount}`);
    expect(checkCount).toBe(2);
  });

  // ── Scenario 8: Delete tender and verify removal ─────────────────────────
  test("Scenario 8: Delete tender and verify it is removed from channel detail and list", async ({
    page,
  }) => {
    const tenderName = uniqueName("مناقصة-للحذف-سيناريو8");

    // Create the tender to delete
    const afterCreateUrl = await createTenderFromChannelUrl(page, CHANNEL_PK, {
      name: tenderName,
    });
    expect(afterCreateUrl).toContain(`/channel/${CHANNEL_PK}/`);

    const bodyAfterCreate = await page.textContent("body");
    expect(bodyAfterCreate).toContain("تم إضافة المناقصة بنجاح");
    expect(bodyAfterCreate).toContain(tenderName);

    // Navigate to channel detail and confirm tender exists
    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();

    const inTableBefore = await channelPage.isTenderInTable(tenderName);
    expect(inTableBefore).toBe(true);

    await channelPage.takeScreenshot("t8_before_delete");

    // Click delete for this tender
    await channelPage.clickDeleteForTender(tenderName);

    // Should land on confirm delete page
    await expect(page.locator("body")).toContainText(tenderName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "t8_confirm_delete.png"),
      fullPage: true,
    });

    // Confirm deletion
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('form[method="post"] button[type="submit"]').click(),
    ]);

    // Should redirect back to channel detail
    expect(page.url()).toContain(`/channel/${CHANNEL_PK}/`);

    // Verify success message
    const bodyAfterDelete = await page.textContent("body");
    expect(bodyAfterDelete).toContain("تم حذف المناقصة بنجاح");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "t8_after_delete.png"),
      fullPage: true,
    });

    // Verify tender is no longer in the channel detail table
    const inTableAfter = await channelPage.isTenderInTable(tenderName);
    expect(inTableAfter).toBe(false);

    // Also verify it is gone from the global list
    await page.goto(TENDER_LIST_URL);
    await page.waitForLoadState("networkidle");

    // Search for the deleted tender name — should not be in list
    const listBodyText = await page.textContent("body");
    expect(listBodyText).not.toContain(tenderName);
  });

  // ── Scenario 9: All 10 boolean stages checked and verified ───────────────
  test("Scenario 9: Create tender with all 10 stages checked, verify 10 checkmarks in list", async ({
    page,
  }) => {
    const tenderName = uniqueName("مناقصة-كاملة-سيناريو9");

    const redirectUrl = await createTenderFromChannelUrl(page, CHANNEL_PK, {
      name: tenderName,
      formalInspectionMinutes: true,
      adminFormationOrder: true,
      technicalMinutes: true,
      minutes1: true,
      technicalReport: true,
      minutes2: true,
      financialOpening: true,
      financialReport: true,
      minutes3: true,
      bidAcceptanceNotification: true,
    });

    expect(redirectUrl).toContain(`/channel/${CHANNEL_PK}/`);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة المناقصة بنجاح");
    expect(bodyText).toContain(tenderName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "t9_all_stages_channel_detail.png"),
      fullPage: true,
    });

    // Verify 10 checkmarks in channel detail
    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();
    const channelCheckCount = await channelPage.getCheckIconCountForTender(tenderName);
    console.log(`Scenario 9 — check icons in channel detail: ${channelCheckCount}`);
    expect(channelCheckCount).toBe(10);

    // Also verify in the global tender list
    const listPage = new TenderListPage(page);
    await listPage.goto();
    const inList = await listPage.isTenderInList(tenderName);
    expect(inList).toBe(true);

    const listCheckCount = await listPage.getCheckIconCountForTender(tenderName);
    console.log(`Scenario 9 — check icons in tender list: ${listCheckCount}`);
    expect(listCheckCount).toBe(10);

    await listPage.takeScreenshot("t9_all_stages_list");
  });
});
