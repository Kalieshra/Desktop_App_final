import { test, expect, Page } from "@playwright/test";
import path from "path";

const BASE_URL = "http://127.0.0.1:8000";
const CHANNEL_PK = 1;
const FORM_URL = `${BASE_URL}/supplies/contract-operation/add/?channel=${CHANNEL_PK}`;
const CHANNEL_DETAIL_URL = `${BASE_URL}/supplies/channel/${CHANNEL_PK}/`;

const ATTACHMENT_FILE = path.join(
  __dirname,
  "artifacts",
  "test_contract_attachment.txt",
);

// ── Page Object Model ─────────────────────────────────────────────────────────

class ContractOperationFormPage {
  constructor(private page: Page) {}

  async goto(channelPk: number = CHANNEL_PK) {
    await this.page.goto(
      `${BASE_URL}/supplies/contract-operation/add/?channel=${channelPk}`,
    );
    await this.page.waitForSelector('form[method="post"]');
  }

  async selectOperationType(value: "supplies" | "maintenance" | "contracting") {
    await this.page.locator("#id_operation_type").selectOption(value);
  }

  async fillOperationName(value: string) {
    await this.page.locator("#id_operation_name").fill(value);
  }

  async fillContractingEntity(value: string) {
    await this.page.locator("#id_contracting_entity").fill(value);
  }

  async fillContractStartDate(value: string) {
    await this.page.locator("#id_contract_start_date").fill(value);
  }

  async selectAssignmentMethod(value: "direct" | "tender" | "") {
    await this.page.locator("#id_assignment_method").selectOption(value);
  }

  async fillTotalAmount(value: string) {
    // Clear first to avoid appending to existing value
    await this.page.locator("#id_total_amount").clear();
    await this.page.locator("#id_total_amount").fill(value);
    // Trigger input event so JS calculator fires
    await this.page.locator("#id_total_amount").dispatchEvent("input");
  }

  async fillAmountPaid(value: string) {
    await this.page.locator("#id_amount_paid").clear();
    await this.page.locator("#id_amount_paid").fill(value);
    await this.page.locator("#id_amount_paid").dispatchEvent("input");
  }

  async fillNotes(value: string) {
    await this.page.locator("#id_notes").fill(value);
  }

  async uploadAttachment(filePath: string) {
    await this.page.locator("#id_attachment").setInputFiles(filePath);
  }

  async getRemainingDisplayText(): Promise<string> {
    return (await this.page.locator("#remaining-display").innerText()).trim();
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

class ChannelDetailPage {
  constructor(private page: Page) {}

  async goto(pk: number = CHANNEL_PK) {
    await this.page.goto(`${BASE_URL}/supplies/channel/${pk}/`);
    await this.page.waitForLoadState("networkidle");
  }

  async getContractOperationsTableText(): Promise<string> {
    const table = this.page.locator("table.table-bordered", {
      has: this.page.locator("th", { hasText: "اسم العملية" }),
    });
    return (await table.innerText()).trim();
  }

  async isContractOperationsTableVisible(): Promise<boolean> {
    const header = this.page.locator("h6", {
      hasText: "بيان أعمال التوريدات/صيانة/مقاولات",
    });
    return await header.first().isVisible();
  }

  async getOperationRowByName(operationName: string) {
    return this.page.locator("tr", { hasText: operationName });
  }

  async getGroupHeaders(): Promise<string[]> {
    // Group header rows have colspan=10 and show the operation type label
    const rows = this.page.locator("tr.table-secondary td");
    const count = await rows.count();
    const headers: string[] = [];
    for (let i = 0; i < count; i++) {
      headers.push((await rows.nth(i).innerText()).trim());
    }
    return headers;
  }

  async getRemainingAmountForOperation(operationName: string): Promise<string> {
    const row = this.page.locator("tr", { hasText: operationName });
    // Remaining amount is the 7th cell (index 6)
    const cells = row.locator("td");
    return (await cells.nth(6).innerText()).trim();
  }

  async clickEditForOperation(operationName: string) {
    const row = this.page.locator("tr", { hasText: operationName });
    await row.locator('a[title="تعديل"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async clickDeleteForOperation(operationName: string) {
    const row = this.page.locator("tr", { hasText: operationName });
    await row.locator('a[title="حذف"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async hasDownloadLinkForOperation(operationName: string): Promise<boolean> {
    // Use .last() to target the most-recently created row when the same name
    // appears multiple times across test runs, then .first() on the button
    // to avoid strict-mode violations if multiple attachments exist in that row.
    const row = this.page.locator("tr", { hasText: operationName }).last();
    const downloadBtn = row
      .locator('a.btn-outline-primary[href*="/media/"]')
      .first();
    return await downloadBtn.isVisible();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: path.join(__dirname, "artifacts", `${name}.png`),
      fullPage: true,
    });
  }
}

// ── Helper: create a ContractOperation via UI ─────────────────────────────────

interface ContractOpData {
  type: "supplies" | "maintenance" | "contracting";
  name: string;
  entity?: string;
  startDate?: string;
  method?: "direct" | "tender" | "";
  total?: string;
  paid?: string;
  notes?: string;
  attachment?: string;
}

async function createContractOperation(
  page: Page,
  data: ContractOpData,
): Promise<string> {
  const formPage = new ContractOperationFormPage(page);
  await formPage.goto();

  await formPage.selectOperationType(data.type);
  await formPage.fillOperationName(data.name);
  if (data.entity) await formPage.fillContractingEntity(data.entity);
  if (data.startDate) await formPage.fillContractStartDate(data.startDate);
  if (data.method !== undefined)
    await formPage.selectAssignmentMethod(data.method);
  if (data.total) await formPage.fillTotalAmount(data.total);
  if (data.paid) await formPage.fillAmountPaid(data.paid);
  if (data.notes) await formPage.fillNotes(data.notes);
  if (data.attachment) await formPage.uploadAttachment(data.attachment);

  return await formPage.submit();
}

// ── Tests ─────────────────────────────────────────────────────────────────────

test.describe("ContractOperation Feature — Django Supplies App", () => {
  test.beforeEach(async ({ page }) => {
    // Verify the server is responding and the channel exists
    const response = await page.goto(CHANNEL_DETAIL_URL);
    expect(response?.status()).toBeLessThan(400);
  });

  // ── Scenario 1: Sidebar link ─────────────────────────────────────────────
  test("Scenario 1: Sidebar contains عملية تعاقد link navigating to /add/", async ({
    page,
  }) => {
    await page.goto(`${BASE_URL}/supplies/`);

    // Verify the sidebar link text
    const sidebarLink = page.locator("nav#sidebar a", {
      hasText: "عملية تعاقد",
    });
    await expect(sidebarLink).toBeVisible();

    // Verify href points to the correct URL
    const href = await sidebarLink.getAttribute("href");
    expect(href).toContain("/supplies/contract-operation/add/");

    // Click and verify navigation
    await sidebarLink.click();
    await page.waitForLoadState("networkidle");
    expect(page.url()).toContain("/supplies/contract-operation/add/");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s1_sidebar_nav.png"),
      fullPage: true,
    });
  });

  // ── Scenario 2: Create ContractOperation (توريدات) ───────────────────────
  test("Scenario 2: Create توريدات operation and verify redirect to channel detail", async ({
    page,
  }) => {
    const formPage = new ContractOperationFormPage(page);
    await formPage.goto();

    await formPage.takeScreenshot("s2_empty_form");

    // Verify form heading
    await expect(page.locator("h3")).toContainText("إضافة عملية تعاقد جديدة");

    // Verify supply_channel is pre-populated (hidden input has value)
    const channelValue = await page.locator("#id_supply_channel").inputValue();
    expect(channelValue).toBe(`${CHANNEL_PK}`);

    // Fill all required and optional fields
    await formPage.selectOperationType("supplies");
    await formPage.fillOperationName("توريد معدات");
    await formPage.fillContractingEntity("شركة الخليج");
    await formPage.fillContractStartDate("2026-01-15");
    await formPage.selectAssignmentMethod("direct");
    await formPage.fillTotalAmount("100000");
    await formPage.fillAmountPaid("60000");
    await formPage.fillNotes("ملاحظة تجريبية");

    await formPage.takeScreenshot("s2_filled_form");

    const redirectUrl = await formPage.submit();

    // Should redirect to channel detail, NOT stay on add form
    expect(redirectUrl).not.toContain("/contract-operation/add/");
    expect(redirectUrl).toContain(`/channel/${CHANNEL_PK}/`);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s2_after_save.png"),
      fullPage: true,
    });

    // Verify success message
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة العملية بنجاح");

    // Verify the operation name appears in the channel detail
    expect(bodyText).toContain("توريد معدات");
  });

  // ── Scenario 3: Live remaining amount calculator ─────────────────────────
  test("Scenario 3: Live calculator shows remaining = total - paid", async ({
    page,
  }) => {
    const formPage = new ContractOperationFormPage(page);
    await formPage.goto();

    // Initially the display should show dash or zero
    const initialText = await formPage.getRemainingDisplayText();
    // Could be "-" or "0.00" depending on initial state — just verify it exists
    expect(initialText).toBeDefined();

    // Enter total=100000 and paid=60000
    await formPage.fillTotalAmount("100000");

    // After filling total only: remaining = 100000 - 0 = 100000
    const afterTotalText = await formPage.getRemainingDisplayText();
    expect(afterTotalText).toBeTruthy();

    await formPage.fillAmountPaid("60000");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s3_calculator.png"),
      fullPage: true,
    });

    // After filling paid: remaining = 100000 - 60000 = 40000
    const remainingText = await formPage.getRemainingDisplayText();

    // The display uses Arabic locale formatting: toLocaleString('ar-EG')
    // This produces Arabic-Indic digits like "٤٠٬٠٠٠٫٠٠" where ٫ is the decimal separator.
    // Strategy: convert Arabic-Indic digits (U+0660–U+0669) to ASCII, then replace the
    // Arabic decimal separator (U+066B or ٫) with '.', strip grouping chars, and parse.
    const normalized = remainingText
      .replace(/[\u0660-\u0669]/g, (d) => String(d.charCodeAt(0) - 0x0660))
      .replace(/[\u066b\u066c٫٬,،]/g, (ch) =>
        ch === "\u066b" || ch === "٫" ? "." : "",
      )
      .replace(/[^\d.]/g, "");
    const numericValue = Math.round(parseFloat(normalized));
    expect(numericValue).toBe(40000);

    // The display class should be text-success (positive balance)
    const displayClass = await page
      .locator("#remaining-display")
      .getAttribute("class");
    expect(displayClass).toContain("text-success");
  });

  // ── Scenario 4: Create ContractOperation (صيانة) ────────────────────────
  test("Scenario 4: Create صيانة operation, verify it appears in channel detail table", async ({
    page,
  }) => {
    const redirectUrl = await createContractOperation(page, {
      type: "maintenance",
      name: "صيانة أجهزة التكييف",
      entity: "شركة البرد",
      startDate: "2026-02-01",
      method: "tender",
      total: "50000",
      paid: "25000",
      notes: "صيانة دورية",
    });

    expect(redirectUrl).toContain(`/channel/${CHANNEL_PK}/`);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة العملية بنجاح");
    expect(bodyText).toContain("صيانة أجهزة التكييف");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s4_maintenance_created.png"),
      fullPage: true,
    });

    // Verify table is visible and contains the operation
    const channelPage = new ChannelDetailPage(page);
    const tableVisible = await channelPage.isContractOperationsTableVisible();
    expect(tableVisible).toBe(true);

    const tableText = await channelPage.getContractOperationsTableText();
    expect(tableText).toContain("صيانة أجهزة التكييف");
  });

  // ── Scenario 5: Create ContractOperation (مقاولات) ──────────────────────
  test("Scenario 5: Create مقاولات operation, verify it appears in channel detail table", async ({
    page,
  }) => {
    const redirectUrl = await createContractOperation(page, {
      type: "contracting",
      name: "إنشاء مبنى إداري",
      entity: "شركة المقاولون العرب",
      startDate: "2026-03-01",
      method: "tender",
      total: "500000",
      paid: "200000",
    });

    expect(redirectUrl).toContain(`/channel/${CHANNEL_PK}/`);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة العملية بنجاح");
    expect(bodyText).toContain("إنشاء مبنى إداري");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s5_contracting_created.png"),
      fullPage: true,
    });

    const channelPage = new ChannelDetailPage(page);
    const tableText = await channelPage.getContractOperationsTableText();
    expect(tableText).toContain("إنشاء مبنى إداري");
  });

  // ── Scenario 6: Channel detail table structure ───────────────────────────
  test("Scenario 6: Channel detail table shows grouped operations with correct remaining amounts", async ({
    page,
  }) => {
    // Create all 3 types to ensure grouping is exercised
    await createContractOperation(page, {
      type: "supplies",
      name: "توريد حاسبات - سيناريو6",
      total: "80000",
      paid: "40000",
    });
    await createContractOperation(page, {
      type: "maintenance",
      name: "صيانة شبكة - سيناريو6",
      total: "30000",
      paid: "15000",
    });
    await createContractOperation(page, {
      type: "contracting",
      name: "تشطيب مكاتب - سيناريو6",
      total: "120000",
      paid: "60000",
    });

    // Navigate to channel detail to inspect the table
    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();

    await channelPage.takeScreenshot("s6_channel_detail_table");

    // Table header must be visible
    const tableVisible = await channelPage.isContractOperationsTableVisible();
    expect(tableVisible).toBe(true);

    // Verify group headers appear (توريدات, صيانة, مقاولات)
    const groupHeaders = await channelPage.getGroupHeaders();
    expect(groupHeaders).toContain("توريدات");
    expect(groupHeaders).toContain("صيانة");
    expect(groupHeaders).toContain("مقاولات");

    // Verify remaining amount for the supplies operation: 80000 - 40000 = 40000
    const remainingSupplies = await channelPage.getRemainingAmountForOperation(
      "توريد حاسبات - سيناريو6",
    );
    // Django renders the decimal as "40000.00"
    expect(remainingSupplies).toContain("40000");

    // Verify remaining amount for maintenance: 30000 - 15000 = 15000
    const remainingMaintenance =
      await channelPage.getRemainingAmountForOperation("صيانة شبكة - سيناريو6");
    expect(remainingMaintenance).toContain("15000");

    // Verify remaining amount for contracting: 120000 - 60000 = 60000
    const remainingContracting =
      await channelPage.getRemainingAmountForOperation(
        "تشطيب مكاتب - سيناريو6",
      );
    expect(remainingContracting).toContain("60000");
  });

  // ── Scenario 7: Edit operation ───────────────────────────────────────────
  test("Scenario 7: Edit operation name and verify change persists", async ({
    page,
  }) => {
    const originalName = "عملية للتعديل - سيناريو7";
    const updatedName = "عملية بعد التعديل - سيناريو7";

    // Create initial operation
    await createContractOperation(page, {
      type: "supplies",
      name: originalName,
      entity: "شركة الاختبار",
      total: "10000",
      paid: "5000",
    });

    // Navigate back to channel detail
    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();

    // Verify original name is present before editing
    const tableTextBefore = await channelPage.getContractOperationsTableText();
    expect(tableTextBefore).toContain(originalName);

    await channelPage.takeScreenshot("s7_before_edit");

    // Click edit for the operation
    await channelPage.clickEditForOperation(originalName);

    // Verify we are on the edit form
    await expect(page.locator("h3")).toContainText("تعديل عملية تعاقد");

    // Change the operation name
    const nameInput = page.locator("#id_operation_name");
    await nameInput.clear();
    await nameInput.fill(updatedName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s7_edit_form.png"),
      fullPage: true,
    });

    // Save
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('button[type="submit"]').click(),
    ]);

    // Verify success message and updated name
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم تعديل العملية بنجاح");
    expect(bodyText).toContain(updatedName);
    expect(bodyText).not.toContain(originalName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s7_after_edit.png"),
      fullPage: true,
    });
  });

  // ── Scenario 8: Delete operation ────────────────────────────────────────
  test("Scenario 8: Delete operation and verify removal from table", async ({
    page,
  }) => {
    const operationName = "عملية للحذف - سيناريو8";

    // Create operation to delete
    await createContractOperation(page, {
      type: "maintenance",
      name: operationName,
      total: "20000",
      paid: "10000",
    });

    // Navigate to channel detail and verify the operation exists
    const channelPage = new ChannelDetailPage(page);
    await channelPage.goto();
    const tableTextBefore = await channelPage.getContractOperationsTableText();
    expect(tableTextBefore).toContain(operationName);

    await channelPage.takeScreenshot("s8_before_delete");

    // Click delete
    await channelPage.clickDeleteForOperation(operationName);

    // We should land on the delete confirmation page
    await expect(page.locator("body")).toContainText(operationName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s8_confirm_delete.png"),
      fullPage: true,
    });

    // Confirm deletion by submitting the confirm form
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('form[method="post"] button[type="submit"]').click(),
    ]);

    // Should redirect back to channel detail
    expect(page.url()).toContain(`/channel/${CHANNEL_PK}/`);

    // Verify the deleted operation is gone
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم حذف العملية بنجاح");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s8_after_delete.png"),
      fullPage: true,
    });

    // Check if the operation name is still on the page
    // (it should NOT be in the table anymore)
    const allText = await page.textContent("body");
    expect(allText).not.toContain(operationName);
  });

  // ── Scenario 9: File attachment ──────────────────────────────────────────
  test("Scenario 9: Create operation with attachment, verify download link in table", async ({
    page,
  }) => {
    const operationName = "توريد مع مرفق - سيناريو9";

    // Create operation with attachment
    await createContractOperation(page, {
      type: "supplies",
      name: operationName,
      entity: "شركة المرفقات",
      total: "75000",
      paid: "25000",
      attachment: ATTACHMENT_FILE,
    });

    expect(page.url()).toContain(`/channel/${CHANNEL_PK}/`);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة العملية بنجاح");
    expect(bodyText).toContain(operationName);

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s9_with_attachment.png"),
      fullPage: true,
    });

    // Verify download link exists for this operation
    const channelPage = new ChannelDetailPage(page);
    const hasDownload =
      await channelPage.hasDownloadLinkForOperation(operationName);
    expect(hasDownload).toBe(true);

    // Also verify the link href contains /media/.
    // Use .last() on the row and .first() on the link to stay strict-mode safe
    // when prior test runs have accumulated rows with the same operation name.
    const row = page.locator("tr", { hasText: operationName }).last();
    const downloadLink = row
      .locator('a.btn-outline-primary[href*="/media/"]')
      .first();
    const href = await downloadLink.getAttribute("href");
    expect(href).toContain("/media/");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "s9_download_link_verified.png"),
      fullPage: true,
    });
  });
});
