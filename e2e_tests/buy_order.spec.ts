import { test, expect, Page } from "@playwright/test";
import path from "path";

const BASE_URL = "http://127.0.0.1:8000";
const CHANNEL_PK = 1;
const FORM_URL = `${BASE_URL}/supplies/buy-order/add/?channel=${CHANNEL_PK}`;

// Paths to test files for upload
const MEMO_FILE = path.join(__dirname, "artifacts", "test_memo.txt");
const ATTACHMENT_FILE = path.join(
  __dirname,
  "artifacts",
  "test_attachment.txt",
);

// ── Page Object Model ─────────────────────────────────────────────────────────

class BuyOrderFormPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto(FORM_URL);
    await this.page.waitForSelector('form[method="post"]');
  }

  async fillRequesterName(value: string) {
    await this.page.locator("#id_requester_name").fill(value);
  }

  async fillLocation(value: string) {
    await this.page.locator("#id_location").fill(value);
  }

  async fillDescription(value: string) {
    await this.page.locator("#id_description").fill(value);
  }

  async fillEstimatedValue(value: string) {
    await this.page.locator("#id_estimated_value").fill(value);
  }

  async fillCompanyEntity(value: string) {
    await this.page.locator("#id_company_entity").fill(value);
  }

  async fillSupplyOrderNo(value: string) {
    await this.page.locator("#id_supply_order_no").fill(value);
  }

  async checkOfferEnvap() {
    await this.page.locator("#id_offer_envap").check();
  }

  async checkOfferFirst() {
    await this.page.locator("#id_offer_first").check();
  }

  async checkOfferThird() {
    await this.page.locator("#id_offer_third").check();
  }

  async checkCommitteeTechnical() {
    await this.page.locator("#id_committee_technical").check();
  }

  async checkCommitteeFinancial() {
    await this.page.locator("#id_committee_financial").check();
  }

  async checkCommitteeSupervisorSignature() {
    await this.page.locator("#id_committee_supervisor_signature").check();
  }

  async uploadMemo(filePath: string) {
    await this.page.locator("#id_memo").setInputFiles(filePath);
  }

  async uploadAttachment(filePath: string) {
    await this.page.locator("#id_attachment").setInputFiles(filePath);
  }

  /**
   * Submit the form and return the URL we land on.
   * After a successful create, Django redirects to channel_detail.
   * We then navigate to the buy_order_detail using the requester name
   * to find the correct row (records are sorted oldest-first in channel_detail).
   */
  async submitAndGoToDetail(requesterName: string): Promise<string> {
    await Promise.all([
      this.page.waitForNavigation({ waitUntil: "networkidle" }),
      this.page.locator('button[type="submit"]').click(),
    ]);

    const landedUrl = this.page.url();
    // If we landed on channel_detail, find the buy_order detail link for this requester
    if (landedUrl.includes("/channel/")) {
      // The channel_detail shows records with buy_order_detail links
      // Find the row that shows this requester name, then click its detail button
      // The records display requester_name in a cell — click the eye icon in that card
      const buyOrderCard = this.page
        .locator(".card", {
          has: this.page.locator(`text="${requesterName}"`),
        })
        .last(); // last = most recent
      const detailLink = buyOrderCard.locator('a[title="التفاصيل"]');
      await detailLink.click();
      await this.page.waitForLoadState("networkidle");
    }

    return this.page.url();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: path.join(__dirname, "artifacts", `${name}.png`),
      fullPage: true,
    });
  }
}

class BuyOrderDetailPage {
  constructor(private page: Page) {}

  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: path.join(__dirname, "artifacts", `${name}.png`),
      fullPage: true,
    });
  }

  /**
   * Get all badge texts in the "العرض" table row.
   * The detail table has <th> cells with Arabic labels and <td> cells with badges.
   */
  async getOfferBadges(): Promise<string[]> {
    // Find the <td> that follows a <th> containing "العرض"
    // In Playwright we can use filter + nth approach
    const rows = this.page.locator("table.table-bordered tbody tr");
    const count = await rows.count();
    for (let i = 0; i < count; i++) {
      const th = rows.nth(i).locator("th");
      const thText = await th.innerText().catch(() => "");
      if (thText.trim() === "العرض") {
        const badges = rows.nth(i).locator(".badge");
        const badgeCount = await badges.count();
        const texts: string[] = [];
        for (let j = 0; j < badgeCount; j++) {
          const text = await badges.nth(j).innerText();
          texts.push(text.trim());
        }
        return texts;
      }
    }
    return [];
  }

  async getCommitteeBadges(): Promise<string[]> {
    const rows = this.page.locator("table.table-bordered tbody tr");
    const count = await rows.count();
    for (let i = 0; i < count; i++) {
      const th = rows.nth(i).locator("th");
      const thText = await th.innerText().catch(() => "");
      if (thText.trim() === "محضر باللجان") {
        const badges = rows.nth(i).locator(".badge");
        const badgeCount = await badges.count();
        const texts: string[] = [];
        for (let j = 0; j < badgeCount; j++) {
          const text = await badges.nth(j).innerText();
          texts.push(text.trim());
        }
        return texts;
      }
    }
    return [];
  }

  async hasMemoDownloadLink(): Promise<boolean> {
    // Looking for: <a href="..." class="btn btn-sm btn-outline-secondary"> with text "تحميل المذكرة"
    const link = this.page.locator("a.btn-outline-secondary", {
      hasText: "تحميل المذكرة",
    });
    return await link.isVisible();
  }

  async hasAttachmentDownloadLink(): Promise<boolean> {
    // Looking for: <a href="..." class="btn btn-sm btn-outline-primary"> with text "تحميل المرفق"
    const link = this.page.locator("a.btn-outline-primary", {
      hasText: "تحميل المرفق",
    });
    return await link.isVisible();
  }

  async getFieldValueByLabel(labelText: string): Promise<string> {
    const rows = this.page.locator("table.table-bordered tbody tr");
    const count = await rows.count();
    for (let i = 0; i < count; i++) {
      const th = rows.nth(i).locator("th");
      const thText = await th.innerText().catch(() => "");
      if (thText.trim() === labelText) {
        const td = rows.nth(i).locator("td");
        return (await td.innerText()).trim();
      }
    }
    return "";
  }
}

// ── Tests ─────────────────────────────────────────────────────────────────────

test.describe("BuyOrder Form — Django Supplies App", () => {
  test.beforeEach(async ({ page }) => {
    const response = await page.goto(`${BASE_URL}/supplies/`);
    expect(response?.status()).toBeLessThan(400);
  });

  // ── Scenario 1: Create BuyOrder with all main fields ────────────────────────
  test("Scenario 1: Create BuyOrder with all required fields", async ({
    page,
  }) => {
    const formPage = new BuyOrderFormPage(page);
    await formPage.goto();

    await formPage.takeScreenshot("01_empty_form");

    // Verify page heading
    await expect(page.locator("h3")).toContainText("إضافة طلب شراء");

    // Verify supply_channel dropdown is pre-selected
    const channelSelect = page.locator("#id_supply_channel");
    await expect(channelSelect).toHaveValue(`${CHANNEL_PK}`);

    // Fill fields
    await formPage.fillRequesterName("أحمد محمد علي - سيناريو1");
    await formPage.fillLocation("مكتب رقم 5 - المبنى الرئيسي");
    await formPage.fillDescription(
      "توريد مستلزمات مكتبية متنوعة للاستخدام الإداري",
    );
    await formPage.fillEstimatedValue("15000.00");
    await formPage.fillCompanyEntity("شركة الخليج للتجارة العامة");
    await formPage.fillSupplyOrderNo("SO-2026-001");

    await formPage.takeScreenshot("01_filled_form");

    // Submit
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('button[type="submit"]').click(),
    ]);

    const currentUrl = page.url();
    // Should NOT still be on the add form
    expect(currentUrl).not.toContain("/buy-order/add/");

    await page.screenshot({
      path: path.join(__dirname, "artifacts", "01_after_save.png"),
      fullPage: true,
    });

    // Page should contain the requester name (on channel_detail timeline)
    const pageText = await page.textContent("body");
    expect(pageText).toContain("أحمد محمد علي");
    expect(pageText).toContain("تم إضافة طلب الشراء بنجاح");
  });

  // ── Scenario 2: Checkbox multi-select العرض ────────────────────────────────
  test("Scenario 2: Check multiple العرض boxes and verify they save", async ({
    page,
  }) => {
    const formPage = new BuyOrderFormPage(page);
    await formPage.goto();

    const requesterName = "فاطمة - سيناريو2";
    await formPage.fillRequesterName(requesterName);

    // Check: عرض Envap, عرض أول, عرض ثالث
    await formPage.checkOfferEnvap();
    await formPage.checkOfferFirst();
    await formPage.checkOfferThird();

    // Verify checked state before submit
    await expect(page.locator("#id_offer_envap")).toBeChecked();
    await expect(page.locator("#id_offer_first")).toBeChecked();
    await expect(page.locator("#id_offer_third")).toBeChecked();
    await expect(page.locator("#id_offer_second")).not.toBeChecked();
    await expect(page.locator("#id_offer_divisible")).not.toBeChecked();

    await formPage.takeScreenshot("02_offer_checkboxes_checked");

    const detailUrl = await formPage.submitAndGoToDetail(requesterName);
    expect(detailUrl).toContain("/buy-order/");
    expect(detailUrl).not.toContain("/add/");

    const detailPage = new BuyOrderDetailPage(page);
    await detailPage.takeScreenshot("02_offer_detail_page");

    // Verify "تفاصيل طلب الشراء" heading
    await expect(page.locator("h3")).toContainText("تفاصيل طلب الشراء");

    // Verify offer badges
    const offerBadges = await detailPage.getOfferBadges();
    console.log("Scenario 2 — Offer badges found:", offerBadges);

    expect(offerBadges).toContain("عرض Envap");
    expect(offerBadges).toContain("عرض أول");
    expect(offerBadges).toContain("عرض ثالث");
    expect(offerBadges).not.toContain("عرض ثان");
    expect(offerBadges).not.toContain("عرض قابل للتجزئة");
  });

  // ── Scenario 3: Checkbox multi-select محضر باللجان ─────────────────────────
  test("Scenario 3: Check multiple محضر باللجان boxes and verify they save", async ({
    page,
  }) => {
    const formPage = new BuyOrderFormPage(page);
    await formPage.goto();

    const requesterName = "محمود - سيناريو3";
    await formPage.fillRequesterName(requesterName);

    // Check: لجنة فنية, ش. مالية, توقيع المشرف
    await formPage.checkCommitteeTechnical();
    await formPage.checkCommitteeFinancial();
    await formPage.checkCommitteeSupervisorSignature();

    await expect(page.locator("#id_committee_technical")).toBeChecked();
    await expect(page.locator("#id_committee_financial")).toBeChecked();
    await expect(
      page.locator("#id_committee_supervisor_signature"),
    ).toBeChecked();
    await expect(page.locator("#id_committee_legal")).not.toBeChecked();
    await expect(
      page.locator("#id_committee_legal_signature"),
    ).not.toBeChecked();

    await formPage.takeScreenshot("03_committee_checkboxes_checked");

    const detailUrl = await formPage.submitAndGoToDetail(requesterName);
    expect(detailUrl).toContain("/buy-order/");
    expect(detailUrl).not.toContain("/add/");

    const detailPage = new BuyOrderDetailPage(page);
    await detailPage.takeScreenshot("03_committee_detail_page");

    await expect(page.locator("h3")).toContainText("تفاصيل طلب الشراء");

    const committeeBadges = await detailPage.getCommitteeBadges();
    console.log("Scenario 3 — Committee badges found:", committeeBadges);

    expect(committeeBadges).toContain("لجنة فنية");
    expect(committeeBadges).toContain("ش. مالية");
    expect(committeeBadges).toContain("توقيع المشرف");
    expect(committeeBadges).not.toContain("ش. قانونية");
    expect(committeeBadges).not.toContain("توقيع ش. قانونية");
  });

  // ── Scenario 4: File attachment upload ────────────────────────────────────
  test("Scenario 4: Upload memo and attachment files, verify download links appear", async ({
    page,
  }) => {
    const formPage = new BuyOrderFormPage(page);
    await formPage.goto();

    const requesterName = "سارة - سيناريو4";
    await formPage.fillRequesterName(requesterName);
    await formPage.fillDescription("طلب شراء مع مستندات مرفقة");

    // Upload files
    await formPage.uploadMemo(MEMO_FILE);
    await formPage.uploadAttachment(ATTACHMENT_FILE);

    await formPage.takeScreenshot("04_files_selected");

    const detailUrl = await formPage.submitAndGoToDetail(requesterName);
    expect(detailUrl).toContain("/buy-order/");
    expect(detailUrl).not.toContain("/add/");

    const detailPage = new BuyOrderDetailPage(page);
    await detailPage.takeScreenshot("04_detail_with_attachments");

    await expect(page.locator("h3")).toContainText("تفاصيل طلب الشراء");

    // Verify download links for memo and attachment
    const hasMemo = await detailPage.hasMemoDownloadLink();
    const hasAttachment = await detailPage.hasAttachmentDownloadLink();

    console.log("Scenario 4 — Has memo download link:", hasMemo);
    console.log("Scenario 4 — Has attachment download link:", hasAttachment);

    expect(hasMemo).toBe(true);
    expect(hasAttachment).toBe(true);

    // Also verify the href attributes have actual file paths
    const memoLink = page.locator("a.btn-outline-secondary", {
      hasText: "تحميل المذكرة",
    });
    const memoHref = await memoLink.getAttribute("href");
    expect(memoHref).toContain("/media/");

    const attachLink = page.locator("a.btn-outline-primary", {
      hasText: "تحميل المرفق",
    });
    const attachHref = await attachLink.getAttribute("href");
    expect(attachHref).toContain("/media/");
  });

  // ── Scenario 5: Full journey — all fields + checkboxes + attachments ────────
  test("Scenario 5: Full journey — all fields, checkboxes, attachments, verify detail page", async ({
    page,
  }) => {
    const formPage = new BuyOrderFormPage(page);
    await formPage.goto();

    const requesterName = "خالد - سيناريو5";

    // Fill all text fields
    await formPage.fillRequesterName(requesterName);
    await formPage.fillLocation("قسم الشراء - الطابق الثالث");
    await formPage.fillDescription(
      "توريد أجهزة حاسوب محمولة للاستخدام الإداري",
    );
    await formPage.fillEstimatedValue("85000.50");
    await formPage.fillCompanyEntity("مؤسسة التقنية الحديثة للتجارة");
    await formPage.fillSupplyOrderNo("SO-2026-FULL-001");

    // Check offer checkboxes
    await formPage.checkOfferEnvap();
    await formPage.checkOfferFirst();
    await formPage.checkOfferThird();

    // Check committee checkboxes
    await formPage.checkCommitteeTechnical();
    await formPage.checkCommitteeFinancial();
    await formPage.checkCommitteeSupervisorSignature();

    // Upload files
    await formPage.uploadMemo(MEMO_FILE);
    await formPage.uploadAttachment(ATTACHMENT_FILE);

    await formPage.takeScreenshot("05_full_form_filled");

    const detailUrl = await formPage.submitAndGoToDetail(requesterName);
    expect(detailUrl).toContain("/buy-order/");
    expect(detailUrl).not.toContain("/add/");

    // Verify the heading confirms we are on buy_order_detail
    await expect(page.locator("h3")).toContainText("تفاصيل طلب الشراء");

    const detailPage = new BuyOrderDetailPage(page);
    await detailPage.takeScreenshot("05_full_detail_page");

    // Verify all text fields saved correctly
    const requesterValue =
      await detailPage.getFieldValueByLabel("اسم مقدم الطلب");
    expect(requesterValue).toBe(requesterName);

    const locationValue = await detailPage.getFieldValueByLabel("المكان");
    expect(locationValue).toBe("قسم الشراء - الطابق الثالث");

    const descriptionValue = await detailPage.getFieldValueByLabel("البيان");
    expect(descriptionValue).toBe("توريد أجهزة حاسوب محمولة للاستخدام الإداري");

    const estimatedValue =
      await detailPage.getFieldValueByLabel("القيمة التقديرية");
    // Django may render decimal with locale-specific separator (e.g. "85000,50" in Arabic locale)
    expect(estimatedValue.replace(",", ".")).toContain("85000.50");

    const companyValue = await detailPage.getFieldValueByLabel("الشركة/الجهة");
    expect(companyValue).toBe("مؤسسة التقنية الحديثة للتجارة");

    const supplyOrderNo = await detailPage.getFieldValueByLabel(
      "استخراج أمر التوريد رقم",
    );
    expect(supplyOrderNo).toBe("SO-2026-FULL-001");

    // Verify offer badges
    const offerBadges = await detailPage.getOfferBadges();
    console.log("Scenario 5 — Offer badges:", offerBadges);
    expect(offerBadges).toContain("عرض Envap");
    expect(offerBadges).toContain("عرض أول");
    expect(offerBadges).toContain("عرض ثالث");

    // Verify committee badges
    const committeeBadges = await detailPage.getCommitteeBadges();
    console.log("Scenario 5 — Committee badges:", committeeBadges);
    expect(committeeBadges).toContain("لجنة فنية");
    expect(committeeBadges).toContain("ش. مالية");
    expect(committeeBadges).toContain("توقيع المشرف");

    // Verify file download links
    const hasMemo = await detailPage.hasMemoDownloadLink();
    const hasAttachment = await detailPage.hasAttachmentDownloadLink();
    expect(hasMemo).toBe(true);
    expect(hasAttachment).toBe(true);

    await detailPage.takeScreenshot("05_final_verification");
  });
});
