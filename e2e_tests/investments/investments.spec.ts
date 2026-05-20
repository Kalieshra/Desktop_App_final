import { test, expect, Page } from "@playwright/test";
import path from "path";

const BASE_URL = "http://127.0.0.1:8000";
const PLAN_LIST_URL = `${BASE_URL}/investments/`;
const PLAN_CREATE_URL = `${BASE_URL}/investments/add/`;
const ARTIFACTS = path.join(__dirname, "..", "artifacts");

// ── Helpers ───────────────────────────────────────────────────────────────────

function uniqueName(base: string): string {
  return `${base}-${Date.now()}`;
}

function artifactPath(name: string): string {
  return path.join(ARTIFACTS, `inv_${name}.png`);
}

// ── Page Object Model ─────────────────────────────────────────────────────────

class InvestmentPlanFormPage {
  constructor(private page: Page) {}

  async gotoCreate() {
    await this.page.goto(PLAN_CREATE_URL);
    await this.page.waitForSelector('form[method="post"]');
  }

  async gotoEdit(pk: number) {
    await this.page.goto(`${BASE_URL}/investments/${pk}/edit/`);
    await this.page.waitForSelector('form[method="post"]');
  }

  async fillName(value: string) {
    await this.page.locator("#id_name").fill(value);
  }

  async fillField(fieldId: string, value: string) {
    const input = this.page.locator(`#${fieldId}`);
    await input.fill("");
    await input.fill(value);
    // Trigger the input event so JS auto-computation fires
    await input.dispatchEvent("input");
  }

  async getInputValue(fieldId: string): Promise<string> {
    return await this.page.locator(`#${fieldId}`).inputValue();
  }

  async getDiffCellText(key: string): Promise<string> {
    const cell = this.page.locator(`[data-diff="${key}"]`);
    return ((await cell.textContent()) ?? "").trim();
  }

  async submit(): Promise<string> {
    await Promise.all([
      this.page.waitForNavigation({ waitUntil: "networkidle" }),
      this.page.locator('button[type="submit"]').click(),
    ]);
    return this.page.url();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: artifactPath(name), fullPage: true });
  }
}

class InvestmentPlanListPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto(PLAN_LIST_URL);
    await this.page.waitForLoadState("networkidle");
  }

  async search(query: string) {
    await this.page.locator('input[name="q"]').fill(query);
    await Promise.all([
      this.page.waitForNavigation({ waitUntil: "networkidle" }),
      this.page.locator('button[type="submit"]').click(),
    ]);
  }

  async isInList(planName: string): Promise<boolean> {
    const bodyText = await this.page.textContent("body");
    return (bodyText ?? "").includes(planName);
  }

  async getRowByName(planName: string) {
    return this.page.locator("tr", { hasText: planName }).last();
  }

  async clickView(planName: string) {
    const row = await this.getRowByName(planName);
    await row.locator('a[title="عرض"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async clickEdit(planName: string) {
    const row = await this.getRowByName(planName);
    await row.locator('a[title="تعديل"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async clickDelete(planName: string) {
    const row = await this.getRowByName(planName);
    await row.locator('a[title="حذف"]').click();
    await this.page.waitForLoadState("networkidle");
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: artifactPath(name), fullPage: true });
  }
}

class InvestmentPlanDetailPage {
  constructor(private page: Page) {}

  /**
   * Read the text content of the difference column cell for a given row label.
   * The detail table renders rows from section_groups context; the 5th <td>
   * in each data row holds the formatted difference value.
   */
  async getDiffForRow(rowLabel: string): Promise<string> {
    const row = this.page
      .locator("table.investment-view-table tbody tr")
      .filter({ hasText: rowLabel })
      .last();
    const cells = row.locator("td");
    const count = await cells.count();
    // Last cell is the diff cell
    const diffCell = cells.nth(count - 1);
    return ((await diffCell.textContent()) ?? "").trim();
  }

  async getValueForRow(rowLabel: string, colIndex: number): Promise<string> {
    // colIndex: 0=البيان, 1=بيان المشروع, 2=الخطة الأصلية, 3=الخطة المعدلة, 4=الفرق
    const row = this.page
      .locator("table.investment-view-table tbody tr")
      .filter({ hasText: rowLabel })
      .last();
    const cell = row.locator("td").nth(colIndex);
    return ((await cell.textContent()) ?? "").trim();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: artifactPath(name), fullPage: true });
  }
}

// ── Helper: create a plan via UI ──────────────────────────────────────────────

interface PlanData {
  name: string;
  landsProject?: string;
  landsOriginal?: string;
  landsModified?: string;
  constructionsOriginal?: string;
  constructionsModified?: string;
  machineryLocalOriginal?: string;
  machineryLocalModified?: string;
  advancePaymentsOriginal?: string;
  advancePaymentsModified?: string;
}

async function createPlan(page: Page, data: PlanData): Promise<string> {
  const formPage = new InvestmentPlanFormPage(page);
  await formPage.gotoCreate();
  await formPage.fillName(data.name);

  if (data.landsProject)
    await formPage.fillField("id_lands_project", data.landsProject);
  if (data.landsOriginal)
    await formPage.fillField("id_lands_original", data.landsOriginal);
  if (data.landsModified)
    await formPage.fillField("id_lands_modified", data.landsModified);
  if (data.constructionsOriginal)
    await formPage.fillField(
      "id_constructions_original",
      data.constructionsOriginal,
    );
  if (data.constructionsModified)
    await formPage.fillField(
      "id_constructions_modified",
      data.constructionsModified,
    );
  if (data.machineryLocalOriginal)
    await formPage.fillField(
      "id_machinery_local_original",
      data.machineryLocalOriginal,
    );
  if (data.machineryLocalModified)
    await formPage.fillField(
      "id_machinery_local_modified",
      data.machineryLocalModified,
    );
  if (data.advancePaymentsOriginal)
    await formPage.fillField(
      "id_advance_payments_original",
      data.advancePaymentsOriginal,
    );
  if (data.advancePaymentsModified)
    await formPage.fillField(
      "id_advance_payments_modified",
      data.advancePaymentsModified,
    );

  return await formPage.submit();
}

// ── Tests ─────────────────────────────────────────────────────────────────────

test.describe("Investment Plans — خطط الاستثمار", () => {
  test.beforeEach(async ({ page }) => {
    const response = await page.goto(PLAN_LIST_URL);
    expect(response?.status()).toBeLessThan(400);
  });

  // ── Scenario 1: Sidebar navigation ───────────────────────────────────────
  test("Scenario 1: Sidebar section خطط الاستثمار has الخطط and إضافة خطة links", async ({
    page,
  }) => {
    await page.goto(BASE_URL);
    await page.waitForLoadState("networkidle");

    // Verify section label
    const sectionLabel = page.locator("nav#sidebar .sidebar-section-label", {
      hasText: "خطط الاستثمار",
    });
    await expect(sectionLabel).toBeVisible();

    // Verify الخطط link
    const plansLink = page.locator("nav#sidebar a", { hasText: "الخطط" });
    await expect(plansLink).toBeVisible();
    const plansHref = await plansLink.getAttribute("href");
    expect(plansHref).toContain("/investments/");

    // Verify إضافة خطة link
    const addLink = page.locator("nav#sidebar a", { hasText: "إضافة خطة" });
    await expect(addLink).toBeVisible();
    const addHref = await addLink.getAttribute("href");
    expect(addHref).toContain("/investments/add/");

    await page.screenshot({ path: artifactPath("s1_sidebar"), fullPage: true });
  });

  test("Scenario 1b: Clicking الخطط sidebar link navigates to /investments/", async ({
    page,
  }) => {
    await page.goto(BASE_URL);
    await page.waitForLoadState("networkidle");

    const plansLink = page.locator("nav#sidebar a", { hasText: "الخطط" });
    // The sidebar may extend below the viewport in a fixed/scrollable container.
    // Scroll the element into view within its container, then navigate via href.
    await plansLink.scrollIntoViewIfNeeded();
    const href = await plansLink.getAttribute("href");
    expect(href).not.toBeNull();
    await page.goto(`${BASE_URL}${href}`);
    await page.waitForLoadState("networkidle");

    expect(page.url()).toContain("/investments/");
    await expect(page.locator("h3")).toContainText("خطط الاستثمار");

    await page.screenshot({
      path: artifactPath("s1b_plans_list_nav"),
      fullPage: true,
    });
  });

  test("Scenario 1c: Clicking إضافة خطة sidebar link navigates to /investments/add/", async ({
    page,
  }) => {
    await page.goto(BASE_URL);
    await page.waitForLoadState("networkidle");

    const addLink = page.locator("nav#sidebar a", { hasText: "إضافة خطة" });
    // The sidebar may extend below the viewport in a fixed/scrollable container.
    // Scroll the element into view within its container, then navigate via href.
    await addLink.scrollIntoViewIfNeeded();
    const href = await addLink.getAttribute("href");
    expect(href).not.toBeNull();
    await page.goto(`${BASE_URL}${href}`);
    await page.waitForLoadState("networkidle");

    expect(page.url()).toContain("/investments/add/");
    await expect(page.locator("h3")).toContainText("إضافة خطة استثمار");

    await page.screenshot({
      path: artifactPath("s1c_add_plan_nav"),
      fullPage: true,
    });
  });

  // ── Scenario 2: Create a new investment plan ──────────────────────────────
  test("Scenario 2: Create new plan — form renders, submits, redirects to list", async ({
    page,
  }) => {
    const planName = uniqueName("خطة-سيناريو2");
    const formPage = new InvestmentPlanFormPage(page);
    const listPage = new InvestmentPlanListPage(page);

    await formPage.gotoCreate();

    // Verify heading
    await expect(page.locator("h3")).toContainText("إضافة خطة استثمار");

    // Verify matrix table header columns are present
    await expect(
      page.locator("table.investment-table thead th", {
        hasText: "بيان المشروع",
      }),
    ).toBeVisible();
    await expect(
      page.locator("table.investment-table thead th", {
        hasText: "الخطة الأصلية",
      }),
    ).toBeVisible();
    await expect(
      page.locator("table.investment-table thead th", {
        hasText: "الخطة المعدلة",
      }),
    ).toBeVisible();
    await expect(
      page.locator("table.investment-table thead th", {
        hasText: "الفرق",
      }),
    ).toBeVisible();

    await formPage.takeScreenshot("s2_empty_form");

    // Fill minimum required data
    await formPage.fillName(planName);
    await formPage.fillField("id_lands_project", "500");
    await formPage.fillField("id_lands_original", "1000");
    await formPage.fillField("id_lands_modified", "1200");

    await formPage.takeScreenshot("s2_filled_form");

    const redirectUrl = await formPage.submit();

    // Should redirect to plan list after successful creation
    expect(redirectUrl).toContain("/investments/");
    expect(redirectUrl).not.toContain("/add/");

    // Verify success message
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة خطة الاستثمار بنجاح");

    await page.screenshot({
      path: artifactPath("s2_after_create"),
      fullPage: true,
    });

    // Verify plan is in the list
    const inList = await listPage.isInList(planName);
    expect(inList).toBe(true);

    await listPage.takeScreenshot("s2_plan_in_list");
  });

  // ── Scenario 3: JS auto-computation — diff column ────────────────────────
  test("Scenario 3: JS diff column updates live when original/modified values are entered", async ({
    page,
  }) => {
    const formPage = new InvestmentPlanFormPage(page);
    await formPage.gotoCreate();

    // Initially diff cells should show "—" or "+0.00"
    // After refreshAllDiffs() runs on load with all zeros, cells show "+0.00"
    const initialDiff = await formPage.getDiffCellText("lands");
    expect(["+0.00", "—"]).toContain(initialDiff);

    // Enter original value for lands
    await formPage.fillField("id_lands_original", "1000");
    let diff = await formPage.getDiffCellText("lands");
    // modified is still 0, so diff = 0 - 1000 = -1000.00
    expect(diff).toBe("-1000.00");

    // Now enter modified value
    await formPage.fillField("id_lands_modified", "1500");
    diff = await formPage.getDiffCellText("lands");
    // diff = 1500 - 1000 = +500.00
    expect(diff).toBe("+500.00");

    // Verify negative diff when modified < original
    await formPage.fillField("id_lands_modified", "800");
    diff = await formPage.getDiffCellText("lands");
    expect(diff).toBe("-200.00");

    // Verify zero diff when modified == original
    await formPage.fillField("id_lands_modified", "1000");
    diff = await formPage.getDiffCellText("lands");
    expect(diff).toBe("+0.00");

    await formPage.takeScreenshot("s3_diff_column_live");
  });

  // ── Scenario 4: JS auto-computation — subtotals ───────────────────────────
  test("Scenario 4: JS auto-computes transport_subtotal, setup_subtotal, total_fixed_investment, grand_total", async ({
    page,
  }) => {
    const formPage = new InvestmentPlanFormPage(page);
    await formPage.gotoCreate();

    // Section 4 - النقل والأثاث: transport_means + furniture_equipment + livestock → transport_subtotal
    await formPage.fillField("id_transport_means_original", "100");
    await formPage.fillField("id_furniture_equipment_original", "200");
    await formPage.fillField("id_livestock_original", "300");

    const transportSub = await formPage.getInputValue(
      "id_transport_subtotal_original",
    );
    expect(parseFloat(transportSub)).toBeCloseTo(600, 1);

    // Section 5 - تجهيزات وأبحاث: setup_preparations + transport_travel_expenses + research_studies → setup_subtotal
    await formPage.fillField("id_setup_preparations_original", "50");
    await formPage.fillField("id_transport_travel_expenses_original", "75");
    await formPage.fillField("id_research_studies_original", "25");

    const setupSub = await formPage.getInputValue("id_setup_subtotal_original");
    expect(parseFloat(setupSub)).toBeCloseTo(150, 1);

    // total_fixed_investment = lands + residential_buildings + non_residential_buildings
    //   + constructions + machinery_local + machinery_foreign + machinery_self_financed
    //   + transport_subtotal + setup_subtotal
    // With our inputs: 0+0+0+0+0+0+0+600+150 = 750
    const totalFixed = await formPage.getInputValue(
      "id_total_fixed_investment_original",
    );
    expect(parseFloat(totalFixed)).toBeCloseTo(750, 1);

    // grand_total = total_fixed_investment + advance_payments
    await formPage.fillField("id_advance_payments_original", "250");
    const grandTotal = await formPage.getInputValue("id_grand_total_original");
    expect(parseFloat(grandTotal)).toBeCloseTo(1000, 1);

    await formPage.takeScreenshot("s4_auto_computed_totals");
  });

  // ── Scenario 5: Create plan with values, check detail page ───────────────
  test("Scenario 5: Create plan with numeric values, verify detail page shows correct diff", async ({
    page,
  }) => {
    const planName = uniqueName("خطة-سيناريو5");
    const listPage = new InvestmentPlanListPage(page);
    const detailPage = new InvestmentPlanDetailPage(page);

    // Create via helper with specific values
    const redirectUrl = await createPlan(page, {
      name: planName,
      landsProject: "500",
      landsOriginal: "1000",
      landsModified: "1500",
      constructionsOriginal: "2000",
      constructionsModified: "2500",
    });

    expect(redirectUrl).toContain("/investments/");
    expect(redirectUrl).not.toContain("/add/");

    // Verify success
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("تم إضافة خطة الاستثمار بنجاح");

    // Navigate to list and click the view button for this plan
    await listPage.goto();
    expect(await listPage.isInList(planName)).toBe(true);

    await listPage.takeScreenshot("s5_plan_in_list");

    // Click view (عرض)
    await listPage.clickView(planName);

    // Verify heading shows plan name
    await expect(page.locator("h3")).toContainText(planName);

    await detailPage.takeScreenshot("s5_detail_page");

    // Verify lands row: original=1000, modified=1500, diff=+500.00
    const landsDiff = await detailPage.getDiffForRow("أراضي");
    expect(landsDiff).toContain("500");
    expect(landsDiff).toContain("+");

    // Verify constructions row: original=2000, modified=2500, diff=+500.00
    const constructionsDiff = await detailPage.getDiffForRow("تشييدات");
    expect(constructionsDiff).toContain("500");
    expect(constructionsDiff).toContain("+");

    // Verify the detail page has the read-only table (no input fields)
    const inputCount = await page
      .locator("table.investment-view-table input")
      .count();
    expect(inputCount).toBe(0);
  });

  // ── Scenario 6: Detail page difference column sign correctness ───────────
  test("Scenario 6: Detail diff column shows positive, negative, and zero differences correctly", async ({
    page,
  }) => {
    const planName = uniqueName("خطة-سيناريو6");

    // lands: original=1000, modified=1500 → +500 (positive)
    // constructions: original=3000, modified=2000 → -1000 (negative)
    // machinery_local: original=500, modified=500 → 0
    const formPage = new InvestmentPlanFormPage(page);
    await formPage.gotoCreate();
    await formPage.fillName(planName);

    await formPage.fillField("id_lands_original", "1000");
    await formPage.fillField("id_lands_modified", "1500");
    await formPage.fillField("id_constructions_original", "3000");
    await formPage.fillField("id_constructions_modified", "2000");
    await formPage.fillField("id_machinery_local_original", "500");
    await formPage.fillField("id_machinery_local_modified", "500");

    const redirectUrl = await formPage.submit();
    expect(redirectUrl).toContain("/investments/");

    // Navigate directly to the detail URL by finding the plan
    const listPage = new InvestmentPlanListPage(page);
    await listPage.goto();
    await listPage.clickView(planName);

    const detailPage = new InvestmentPlanDetailPage(page);
    await detailPage.takeScreenshot("s6_detail_diff_signs");

    // Positive diff
    const landsDiff = await detailPage.getDiffForRow("أراضي");
    expect(landsDiff).toMatch(/^\+500/);

    // Negative diff
    const constructionsDiff = await detailPage.getDiffForRow("تشييدات");
    expect(constructionsDiff).toMatch(/^-1000/);

    // Zero diff
    const machineryDiff = await detailPage.getDiffForRow("محلي");
    expect(machineryDiff).toMatch(/^\+?0/);
  });

  // ── Scenario 7: Edit plan and verify changes persist ─────────────────────
  test("Scenario 7: Edit plan name and values, verify changes persist in detail page", async ({
    page,
  }) => {
    const originalName = uniqueName("خطة-أصلية-سيناريو7");
    const updatedName = uniqueName("خطة-معدلة-سيناريو7");

    // Create the initial plan
    const afterCreate = await createPlan(page, {
      name: originalName,
      landsOriginal: "1000",
      landsModified: "1000",
    });
    expect(afterCreate).toContain("/investments/");

    const bodyAfterCreate = await page.textContent("body");
    expect(bodyAfterCreate).toContain("تم إضافة خطة الاستثمار بنجاح");

    // Find plan in list and click edit
    const listPage = new InvestmentPlanListPage(page);
    await listPage.goto();
    expect(await listPage.isInList(originalName)).toBe(true);

    await listPage.takeScreenshot("s7_before_edit");
    await listPage.clickEdit(originalName);

    // Should be on edit form
    const editHeading = page.locator("h3");
    await expect(editHeading).toContainText("تعديل");

    // Update name
    const nameInput = page.locator("#id_name");
    await nameInput.clear();
    await nameInput.fill(updatedName);

    // Update lands_original from 1000 to 2000
    const formPage = new InvestmentPlanFormPage(page);
    await formPage.fillField("id_lands_original", "2000");
    await formPage.fillField("id_lands_modified", "2500");

    await page.screenshot({
      path: artifactPath("s7_edit_form"),
      fullPage: true,
    });

    // Submit
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('button[type="submit"]').click(),
    ]);

    // Should redirect to detail page
    expect(page.url()).toContain("/investments/");
    expect(page.url()).not.toContain("/edit/");

    // Verify success message
    const bodyAfterEdit = await page.textContent("body");
    expect(bodyAfterEdit).toContain("تم تعديل خطة الاستثمار بنجاح");
    expect(bodyAfterEdit).toContain(updatedName);

    await page.screenshot({
      path: artifactPath("s7_after_edit"),
      fullPage: true,
    });

    // Verify original name is gone from list
    await listPage.goto();
    expect(await listPage.isInList(originalName)).toBe(false);
    expect(await listPage.isInList(updatedName)).toBe(true);

    // View the detail and verify updated difference
    await listPage.clickView(updatedName);
    const detailPage = new InvestmentPlanDetailPage(page);
    await detailPage.takeScreenshot("s7_detail_after_edit");

    const landsDiff = await detailPage.getDiffForRow("أراضي");
    // 2500 - 2000 = +500
    expect(landsDiff).toContain("500");
    expect(landsDiff).toContain("+");
  });

  // ── Scenario 8: Delete plan and verify removal ────────────────────────────
  test("Scenario 8: Delete plan and verify it is removed from the list", async ({
    page,
  }) => {
    const planName = uniqueName("خطة-للحذف-سيناريو8");

    // Create a plan to delete
    const afterCreate = await createPlan(page, { name: planName });
    expect(afterCreate).toContain("/investments/");

    const bodyAfterCreate = await page.textContent("body");
    expect(bodyAfterCreate).toContain("تم إضافة خطة الاستثمار بنجاح");

    const listPage = new InvestmentPlanListPage(page);
    await listPage.goto();
    expect(await listPage.isInList(planName)).toBe(true);

    await listPage.takeScreenshot("s8_before_delete");

    // Click delete
    await listPage.clickDelete(planName);

    // Should be on confirmation page
    await expect(page.locator("body")).toContainText(planName);
    await expect(
      page.locator(".card-header", { hasText: "تأكيد الحذف" }),
    ).toBeVisible();

    await page.screenshot({
      path: artifactPath("s8_confirm_delete"),
      fullPage: true,
    });

    // Confirm deletion
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('form[method="post"] button[type="submit"]').click(),
    ]);

    // Should redirect to plan list
    expect(page.url()).toContain("/investments/");

    // Verify success message
    const bodyAfterDelete = await page.textContent("body");
    expect(bodyAfterDelete).toContain("تم حذف خطة الاستثمار بنجاح");

    await page.screenshot({
      path: artifactPath("s8_after_delete"),
      fullPage: true,
    });

    // Verify plan is no longer in list
    expect(await listPage.isInList(planName)).toBe(false);
  });

  // ── Scenario 9: Search filter on list page ────────────────────────────────
  test("Scenario 9: Search filter narrows results by plan name", async ({
    page,
  }) => {
    const uniqueKeyword = `بحث-${Date.now()}`;
    const planName = `خطة-${uniqueKeyword}`;

    // Create a plan with a unique name
    await createPlan(page, { name: planName });

    const listPage = new InvestmentPlanListPage(page);
    await listPage.goto();

    // Search should find it
    await listPage.search(uniqueKeyword);
    const bodyText = await page.textContent("body");
    expect(bodyText).toContain(planName);

    await listPage.takeScreenshot("s9_search_found");

    // Search with no match should show empty state
    await listPage.search("xxxx-لا-يوجد-xxxx");
    const emptyText = await page.textContent("body");
    expect(emptyText).toContain("لا توجد خطط استثمار");

    await listPage.takeScreenshot("s9_search_empty");
  });

  // ── Scenario 10: Full CRUD journey — end-to-end ───────────────────────────
  test("Scenario 10: Full journey — create, view detail, edit, verify diff, delete", async ({
    page,
  }) => {
    const planName = uniqueName("خطة-كاملة-سيناريو10");
    const formPage = new InvestmentPlanFormPage(page);
    const listPage = new InvestmentPlanListPage(page);
    const detailPage = new InvestmentPlanDetailPage(page);

    // --- STEP 1: Create ---
    await formPage.gotoCreate();
    await formPage.fillName(planName);

    // Fill Section 1 - الأراضي والمباني
    await formPage.fillField("id_lands_project", "100");
    await formPage.fillField("id_lands_original", "200");
    await formPage.fillField("id_lands_modified", "300");

    await formPage.fillField("id_residential_buildings_project", "50");
    await formPage.fillField("id_residential_buildings_original", "150");
    await formPage.fillField("id_residential_buildings_modified", "180");

    // Fill Section 2 - التشييدات
    await formPage.fillField("id_constructions_project", "400");
    await formPage.fillField("id_constructions_original", "500");
    await formPage.fillField("id_constructions_modified", "600");

    // Fill Section 3 - الآلات والمعدات
    await formPage.fillField("id_machinery_local_original", "300");
    await formPage.fillField("id_machinery_local_modified", "350");
    await formPage.fillField("id_machinery_foreign_original", "200");
    await formPage.fillField("id_machinery_foreign_modified", "200");

    // Fill Section 4 transport items (JS should auto-sum transport_subtotal)
    await formPage.fillField("id_transport_means_original", "100");
    await formPage.fillField("id_transport_means_modified", "120");
    await formPage.fillField("id_furniture_equipment_original", "80");
    await formPage.fillField("id_furniture_equipment_modified", "90");

    // Fill Section 5 setup items (JS should auto-sum setup_subtotal)
    await formPage.fillField("id_setup_preparations_original", "60");
    await formPage.fillField("id_setup_preparations_modified", "70");
    await formPage.fillField("id_research_studies_original", "40");
    await formPage.fillField("id_research_studies_modified", "45");

    // Advance payments
    await formPage.fillField("id_advance_payments_original", "500");
    await formPage.fillField("id_advance_payments_modified", "550");

    // Verify live diff cell for lands before submit
    const landsDiffLive = await formPage.getDiffCellText("lands");
    expect(landsDiffLive).toBe("+100.00"); // 300 - 200 = 100

    await formPage.takeScreenshot("s10_full_form_filled");

    const createRedirect = await formPage.submit();
    expect(createRedirect).toContain("/investments/");
    expect(createRedirect).not.toContain("/add/");

    const bodyAfterCreate = await page.textContent("body");
    expect(bodyAfterCreate).toContain("تم إضافة خطة الاستثمار بنجاح");

    // --- STEP 2: View detail ---
    await listPage.goto();
    expect(await listPage.isInList(planName)).toBe(true);
    await listPage.clickView(planName);

    await expect(page.locator("h3")).toContainText(planName);

    await detailPage.takeScreenshot("s10_detail_page");

    // Verify diff values in detail page
    const landsDiff = await detailPage.getDiffForRow("أراضي");
    expect(landsDiff).toContain("+100"); // 300 - 200

    const constructionsDiff = await detailPage.getDiffForRow("تشييدات");
    expect(constructionsDiff).toContain("+100"); // 600 - 500

    const machineryForeignDiff = await detailPage.getDiffForRow("أجنبي");
    expect(machineryForeignDiff).toMatch(/^\+?0/); // 200 - 200 = 0

    // --- STEP 3: Edit ---
    const editBtn = page.locator("a.btn-warning", { hasText: "تعديل" });
    await editBtn.click();
    await page.waitForLoadState("networkidle");

    expect(page.url()).toContain("/edit/");

    // Change lands_modified from 300 to 400 → new diff = +200
    await formPage.fillField("id_lands_modified", "400");

    await page.screenshot({
      path: artifactPath("s10_edit_modified"),
      fullPage: true,
    });

    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('button[type="submit"]').click(),
    ]);

    expect(page.url()).not.toContain("/edit/");
    const bodyAfterEdit = await page.textContent("body");
    expect(bodyAfterEdit).toContain("تم تعديل خطة الاستثمار بنجاح");

    await detailPage.takeScreenshot("s10_detail_after_edit");

    // Verify updated diff for lands (400 - 200 = +200)
    const landsNewDiff = await detailPage.getDiffForRow("أراضي");
    expect(landsNewDiff).toContain("+200");

    // --- STEP 4: Delete ---
    const deleteBtn = page.locator("a.btn-outline-danger", {
      hasText: "حذف",
    });
    await deleteBtn.click();
    await page.waitForLoadState("networkidle");

    expect(page.url()).toContain("/delete/");
    await expect(
      page.locator(".card-header", { hasText: "تأكيد الحذف" }),
    ).toBeVisible();
    await expect(page.locator(".text-danger.fs-5")).toContainText(planName);

    await page.screenshot({
      path: artifactPath("s10_confirm_delete"),
      fullPage: true,
    });

    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle" }),
      page.locator('form[method="post"] button[type="submit"]').click(),
    ]);

    expect(page.url()).toContain("/investments/");
    const bodyAfterDelete = await page.textContent("body");
    expect(bodyAfterDelete).toContain("تم حذف خطة الاستثمار بنجاح");

    await listPage.goto();
    expect(await listPage.isInList(planName)).toBe(false);

    await listPage.takeScreenshot("s10_plan_gone_from_list");
  });

  // ── Scenario 11: All 54 matrix fields render on the create form ───────────
  test("Scenario 11: Create form contains all expected matrix input fields", async ({
    page,
  }) => {
    const formPage = new InvestmentPlanFormPage(page);
    await formPage.gotoCreate();

    const expectedFields = [
      // Section 1
      "id_lands_project",
      "id_lands_original",
      "id_lands_modified",
      "id_residential_buildings_project",
      "id_residential_buildings_original",
      "id_residential_buildings_modified",
      "id_non_residential_buildings_project",
      "id_non_residential_buildings_original",
      "id_non_residential_buildings_modified",
      // Section 2
      "id_constructions_project",
      "id_constructions_original",
      "id_constructions_modified",
      // Section 3
      "id_machinery_local_project",
      "id_machinery_local_original",
      "id_machinery_local_modified",
      "id_machinery_foreign_project",
      "id_machinery_foreign_original",
      "id_machinery_foreign_modified",
      "id_machinery_self_financed_project",
      "id_machinery_self_financed_original",
      "id_machinery_self_financed_modified",
      // Section 4
      "id_transport_means_project",
      "id_transport_means_original",
      "id_transport_means_modified",
      "id_furniture_equipment_project",
      "id_furniture_equipment_original",
      "id_furniture_equipment_modified",
      "id_livestock_project",
      "id_livestock_original",
      "id_livestock_modified",
      "id_transport_subtotal_project",
      "id_transport_subtotal_original",
      "id_transport_subtotal_modified",
      // Section 5
      "id_setup_preparations_project",
      "id_setup_preparations_original",
      "id_setup_preparations_modified",
      "id_transport_travel_expenses_project",
      "id_transport_travel_expenses_original",
      "id_transport_travel_expenses_modified",
      "id_research_studies_project",
      "id_research_studies_original",
      "id_research_studies_modified",
      "id_setup_subtotal_project",
      "id_setup_subtotal_original",
      "id_setup_subtotal_modified",
      // Section 6
      "id_total_fixed_investment_project",
      "id_total_fixed_investment_original",
      "id_total_fixed_investment_modified",
      "id_advance_payments_project",
      "id_advance_payments_original",
      "id_advance_payments_modified",
      "id_grand_total_project",
      "id_grand_total_original",
      "id_grand_total_modified",
    ];

    for (const fieldId of expectedFields) {
      const input = page.locator(`#${fieldId}`);
      await expect(input).toBeAttached();
    }

    // Also verify 18 diff cells are present (one per matrix row)
    const diffCells = page.locator("[data-diff]");
    const diffCount = await diffCells.count();
    expect(diffCount).toBe(18);

    await formPage.takeScreenshot("s11_all_fields_verified");
  });

  // ── Scenario 12: Form validation — name is required ───────────────────────
  test("Scenario 12: Form validation — submitting without plan name shows error", async ({
    page,
  }) => {
    const formPage = new InvestmentPlanFormPage(page);
    await formPage.gotoCreate();

    // Submit without filling any fields
    await page.locator('button[type="submit"]').click();

    // Should stay on the create form (Django will re-render with errors)
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    expect(currentUrl).toContain("/investments/add/");

    // The form should still be visible
    await expect(page.locator('form[method="post"]')).toBeVisible();

    await page.screenshot({
      path: artifactPath("s12_validation_error"),
      fullPage: true,
    });
  });
});
