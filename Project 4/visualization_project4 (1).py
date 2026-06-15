"""
DecodeLabs Data Analytics Internship — Batch 2026
Project 4: Data Visualization
Author: Anuradha Prasad
Description: 6 professional charts from e-commerce order dataset
             communicating key business insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── Load & Prepare Data ────────────────────────────────────
df = pd.read_excel('Dataset_for_Data_Analytics.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M').astype(str)
df['CouponCode'] = df['CouponCode'].fillna('No Coupon')

# ── Global Style Configuration ─────────────────────────────
DARK      = '#1A3C34'
TEAL      = '#0D6E6E'
ACCENT    = '#27AE60'
LIGHT_BG  = '#F7FAF9'
GRID_COL  = '#E0EBE8'
TEXT_DARK = '#1C2833'
TEXT_MID  = '#555555'
WHITE     = '#FFFFFF'
HIGHLIGHT = '#E74C3C'
ORANGE    = '#E67E22'

plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'axes.facecolor':     LIGHT_BG,
    'figure.facecolor':   WHITE,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.spines.left':   False,
    'axes.spines.bottom': False,
    'axes.grid':          True,
    'grid.color':         GRID_COL,
    'grid.linewidth':     0.6,
    'xtick.color':        TEXT_MID,
    'ytick.color':        TEXT_MID,
    'xtick.labelsize':    9,
    'ytick.labelsize':    9,
})

def add_footer(ax, fig, insight, source='DecodeLabs Data Analytics · Batch 2026'):
    fig.text(0.07, 0.01, insight, fontsize=8, color=TEXT_MID, fontstyle='italic', ha='left')
    fig.text(0.95, 0.01, source, fontsize=7.5, color='#AAAAAA', ha='right')

def styled_title(ax, title, subtitle=''):
    ax.set_title(title, fontsize=13, fontweight='bold', color=DARK, pad=14, loc='left')
    if subtitle:
        ax.annotate(subtitle, xy=(0, 1.04), xycoords='axes fraction', fontsize=9, color=TEXT_MID, ha='left')


# ══════════════════════════════════════════════════════════
# CHART 1 — Revenue by Product
# ══════════════════════════════════════════════════════════
prod = df.groupby('Product')['TotalPrice'].sum().sort_values()
colors_p = [HIGHLIGHT if v == prod.max() else TEAL for v in prod.values]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(prod.index, prod.values, color=colors_p, height=0.55, edgecolor='none', zorder=3)
ax.set_xlim(0, prod.max() * 1.22)
ax.tick_params(length=0)
ax.grid(axis='x', zorder=0)
ax.grid(axis='y', visible=False)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 2500, bar.get_y() + bar.get_height()/2,
            f'₹{w:,.0f}', va='center', ha='left', fontsize=8.5, color=TEXT_DARK, fontweight='500')

styled_title(ax, 'Chair & Printer Lead Revenue — Together ₹3.91L of ₹12.65L Total',
             'Revenue by Product Category  |  Jan 2023 – Jun 2025')
legend = [mpatches.Patch(color=HIGHLIGHT, label='Top performer'),
          mpatches.Patch(color=TEAL, label='Other products')]
ax.legend(handles=legend, loc='lower right', fontsize=8.5, framealpha=0.6, edgecolor='none')
add_footer(ax, fig, 'Insight: Chair & Printer contribute ~15.5% each — prioritise inventory & bundling for these categories.')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('chart1_revenue_by_product.png', dpi=180, bbox_inches='tight')
plt.close()
print('Chart 1 saved.')


# ══════════════════════════════════════════════════════════
# CHART 2 — Monthly Revenue Trend
# ══════════════════════════════════════════════════════════
monthly = df.groupby('Month')['TotalPrice'].sum().reset_index()
monthly.columns = ['Month', 'Revenue']
peak_idx   = monthly['Revenue'].idxmax()
trough_idx = monthly['Revenue'].idxmin()

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(range(len(monthly)), monthly['Revenue'], alpha=0.12, color=TEAL, zorder=1)
ax.plot(range(len(monthly)), monthly['Revenue'], color=TEAL, linewidth=2.2, zorder=3,
        marker='o', markersize=4, markerfacecolor=WHITE, markeredgewidth=1.5, markeredgecolor=TEAL)

ax.annotate(f"Peak\n₹{monthly.loc[peak_idx,'Revenue']:,.0f}",
            xy=(peak_idx, monthly.loc[peak_idx,'Revenue']),
            xytext=(peak_idx - 2.5, monthly.loc[peak_idx,'Revenue'] - 8000),
            fontsize=8, color=HIGHLIGHT, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=HIGHLIGHT, lw=1.2), ha='center')
ax.annotate(f"Low\n₹{monthly.loc[trough_idx,'Revenue']:,.0f}",
            xy=(trough_idx, monthly.loc[trough_idx,'Revenue']),
            xytext=(trough_idx + 2.5, monthly.loc[trough_idx,'Revenue'] + 8000),
            fontsize=8, color=ORANGE, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2), ha='center')

for i, (ys, ye, yl) in enumerate([(0, 12,'2023'), (12, 24,'2024'), (24, 30,'2025')]):
    ax.axvspan(ys - 0.5, ye - 0.5, alpha=0.04,
               color=[DARK, TEAL, ACCENT][i], zorder=0)
    ax.text((ys + ye)/2 - 0.5, monthly['Revenue'].max() * 1.01,
            yl, ha='center', fontsize=9, color=TEXT_MID, fontweight='500')

xticks = list(range(0, len(monthly), 3))
ax.set_xticks(xticks)
ax.set_xticklabels([monthly.loc[i,'Month'][-5:] for i in xticks], rotation=30, ha='right', fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
ax.set_ylabel('Monthly Revenue (₹)', fontsize=9, color=TEXT_MID)
ax.tick_params(length=0)
ax.set_xlim(-0.5, len(monthly) - 0.5)

styled_title(ax, 'Revenue Peaks Every Mid-Year — June 2024 Hit ₹68K (Highest Month)',
             'Monthly Revenue Trend  |  Jan 2023 – Jun 2025  |  30 months')
add_footer(ax, fig, 'Insight: May–June consistently spikes — launch seasonal promotions in April to amplify this trend.')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('chart2_monthly_trend.png', dpi=180, bbox_inches='tight')
plt.close()
print('Chart 2 saved.')


# ══════════════════════════════════════════════════════════
# CHART 3 — Order Status Donut Chart
# ══════════════════════════════════════════════════════════
status = df['OrderStatus'].value_counts()
DONUT_COLORS = [HIGHLIGHT, ORANGE, '#F1C40F', TEAL, ACCENT]
EXPLODE = [0.05 if s in ['Cancelled','Returned'] else 0 for s in status.index]

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_facecolor(WHITE)
fig.patch.set_facecolor(WHITE)

wedges, texts, autotexts = ax.pie(
    status.values, autopct='%1.1f%%', colors=DONUT_COLORS,
    startangle=90, explode=EXPLODE, pctdistance=0.78,
    wedgeprops=dict(width=0.52, edgecolor=WHITE, linewidth=2.5))

for t in autotexts:
    t.set_fontsize(9)
    t.set_fontweight('bold')
    t.set_color(WHITE)

ax.text(0, 0.08, '41.4%', ha='center', va='center', fontsize=22, fontweight='bold', color=HIGHLIGHT)
ax.text(0, -0.18, 'Revenue\nLeakage', ha='center', va='center', fontsize=9, color=TEXT_MID, linespacing=1.4)

legend_labels = [f'{s}  —  {v} orders' for s, v in zip(status.index, status.values)]
legend_patches = [mpatches.Patch(color=c, label=l) for c, l in zip(DONUT_COLORS, legend_labels)]
ax.legend(handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, -0.12),
          ncol=2, fontsize=8.5, framealpha=0, edgecolor='none')

ax.set_title('41.4% of All Orders Are Cancelled or Returned — Critical Revenue Crisis',
             fontsize=12, fontweight='bold', color=DARK, pad=14)
add_footer(ax, fig, 'Insight: 497 of 1,200 orders never generated revenue. Immediate investigation of cancellation reasons required.')

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('chart3_order_status.png', dpi=180, bbox_inches='tight')
plt.close()
print('Chart 3 saved.')


# ══════════════════════════════════════════════════════════
# CHART 4 — Revenue by Referral Source
# ══════════════════════════════════════════════════════════
ref = df.groupby('ReferralSource')['TotalPrice'].sum().sort_values()
ref_count = df.groupby('ReferralSource').size()
colors_r = [HIGHLIGHT if i == ref.index[-1] else TEAL for i in ref.index]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(ref.index, ref.values, color=colors_r, height=0.5, edgecolor='none', zorder=3)
ax.set_xlim(0, ref.max() * 1.28)
ax.tick_params(length=0)
ax.grid(axis='x', zorder=0)
ax.grid(axis='y', visible=False)

for bar, idx in zip(bars, ref.index):
    w = bar.get_width()
    ax.text(w + 2000, bar.get_y() + bar.get_height()/2,
            f'₹{w:,.0f}  ({ref_count[idx]} orders)', va='center', ha='left', fontsize=8.5, color=TEXT_DARK, fontweight='500')

legend = [mpatches.Patch(color=HIGHLIGHT, label='Top channel'),
          mpatches.Patch(color=TEAL, label='Other channels')]
ax.legend(handles=legend, loc='lower right', fontsize=8.5, framealpha=0.6, edgecolor='none')
styled_title(ax, 'Instagram Is the #1 Revenue Channel — ₹2.75L Across 259 Orders',
             'Total Revenue & Order Volume by Referral Source')
add_footer(ax, fig, 'Insight: Instagram outperforms all channels. Scale with influencer marketing & product reels.')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('chart4_referral_revenue.png', dpi=180, bbox_inches='tight')
plt.close()
print('Chart 4 saved.')


# ══════════════════════════════════════════════════════════
# CHART 5 — Avg Order Value by Payment Method
# ══════════════════════════════════════════════════════════
pay = df.groupby('PaymentMethod')['TotalPrice'].mean().sort_values(ascending=False)
overall_mean = df['TotalPrice'].mean()
colors_pay = [HIGHLIGHT if i == pay.index[0] else TEAL for i in pay.index]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(pay.index, pay.values, color=colors_pay, width=0.5, edgecolor='none', zorder=3)
ax.axhline(overall_mean, color='#888888', linewidth=1.2, linestyle='--', zorder=2)
ax.text(len(pay) - 0.4, overall_mean + 8, f'Overall avg  ₹{overall_mean:,.0f}',
        fontsize=8.5, color='#888888', ha='right', fontstyle='italic')

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 15,
            f'₹{h:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=TEXT_DARK)

ax.set_ylim(0, pay.max() * 1.18)
ax.set_ylabel('Average Order Value (₹)', fontsize=9, color=TEXT_MID)
ax.tick_params(length=0)
ax.grid(axis='y', zorder=0)
ax.grid(axis='x', visible=False)

legend = [mpatches.Patch(color=HIGHLIGHT, label='Highest avg order value'),
          mpatches.Patch(color=TEAL, label='Other methods')]
ax.legend(handles=legend, loc='upper right', fontsize=8.5, framealpha=0.6, edgecolor='none')
styled_title(ax, 'Credit Card Users Spend 6.9% More Per Order Than the Average',
             'Average Order Value (₹) by Payment Method')
add_footer(ax, fig, 'Insight: Credit Card avg = ₹1,127.55 vs ₹1,053.97 overall. Offer EMI/credit deals to grow basket size.')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('chart5_payment_method.png', dpi=180, bbox_inches='tight')
plt.close()
print('Chart 5 saved.')


# ══════════════════════════════════════════════════════════
# CHART 6 — Correlation Heatmap
# ══════════════════════════════════════════════════════════
num_cols = ['Quantity', 'UnitPrice', 'TotalPrice', 'ItemsInCart']
corr = df[num_cols].corr()
rename_map = {'Quantity': 'Quantity\n(units)', 'UnitPrice': 'Unit Price\n(₹)',
              'TotalPrice': 'Total Price\n(₹)', 'ItemsInCart': 'Items\nin Cart'}
corr.index   = [rename_map[c] for c in corr.index]
corr.columns = [rename_map[c] for c in corr.columns]

fig, ax = plt.subplots(figsize=(7, 5.5))
ax.set_facecolor(WHITE)
cmap = sns.diverging_palette(145, 10, as_cmap=True)
hm = sns.heatmap(corr, annot=True, fmt='.3f', cmap=cmap, vmin=-1, vmax=1, center=0,
                 ax=ax, linewidths=2, linecolor=WHITE, annot_kws={'size': 11, 'weight': 'bold'},
                 square=True, cbar_kws={'shrink': 0.72, 'pad': 0.03})

for i in range(len(corr)):
    for j in range(len(corr.columns)):
        val = corr.iloc[i, j]
        color = WHITE if abs(val) >= 0.4 else TEXT_MID
        ax.texts[i * len(corr.columns) + j].set_color(color)

ax.tick_params(left=False, bottom=False)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=9)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=9, rotation=0)
hm.collections[0].colorbar.set_label('Pearson r', fontsize=8.5, color=TEXT_MID)

styled_title(ax, 'Unit Price Is the Strongest Revenue Driver — Correlation r = 0.717',
             'Pearson Correlation Matrix  |  Numeric Variables')
add_footer(ax, fig, 'Insight: UnitPrice→TotalPrice (r=0.717). Premium pricing strategy = higher revenue per order.')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('chart6_correlation_heatmap.png', dpi=180, bbox_inches='tight')
plt.close()
print('Chart 6 saved.')

print('\nAll 6 charts generated successfully!')
print('Files: chart1_revenue_by_product.png through chart6_correlation_heatmap.png')
