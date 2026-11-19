"""
gen_runway.py - writes the Runway cluster layout (apps/cluster_themes/hud/layouts/runway.json). Edit this, not the JSON.

    python3 tools/gen_runway.py apps/cluster_themes/hud/layouts/runway.json

Runway: two rev bars that lean apart towards the driver like a runway seen from the cockpit, the gear, drive mode and
speed between them, two ring gauges on the right, a G-meter (or four readouts) on the left, a top bar with the range
and what is playing, and a bottom row with two segmented bars, the clock and the outside temperature. The bars, rings,
segmented bars and lines are one shader (shaders.js runway); everything else is text on top.
"""
import json
import sys

BAR_Y = (100, 610)          # the bars' top and bottom rows
MID = 960                   # the mirror line
BAR = (738, 848, 584, 796)  # the left bar: outer x and inner x at the top, outer x and inner x at the bottom

# font cell heights (tools/bake_fonts.py prints them)
H = {'w_big': 99, 'w_num2': 37, 'w_val': 34, 'w_mid': 51, 'w_label': 28, 'w_title': 40, 'r_label': 30}

W = []


def text(id, x, y, w, font, txt, color='fg', align='center', **kw):
    d = {'id': id, 'type': 'text', 'z': 5, 'x': int(round(x)), 'y': int(round(y)), 'w': int(round(w)), 'h': H[font],
         'text': txt, 'font': font, 'color': color, 'align': align}
    d.update(kw)
    W.append(d)


# ---- the backdrop: one shader -------------------------------------------------------------------------------------
RINGS = [{'cx': 1500, 'cy': 390, 'r': 94, 'slot': 'r1'}, {'cx': 1752, 'cy': 390, 'r': 94, 'slot': 'r2'}]
MTRS = [{'x': 215, 'y': 640, 'w': 300, 'slot': 'b1'}, {'x': 1480, 'y': 640, 'w': 290, 'slot': 'b2'}]
LINES = [
    [600, 80, 1320, 80],        # the top bar's underline
    [830, 34, 830, 80],         # its divider
    [545, 644, 1400, 644],      # the bottom row's line, between the two bars
]
W.append({'id': 'runway', 'type': 'runway', 'class': 'content', 'z': 0, 'x': 0, 'y': 0, 'w': 1920, 'h': 660,
          'bars': list(BAR), 'barY': [BAR_Y[0], BAR_Y[1], MID], 'font': 'w_num2', 'rings': RINGS, 'mtrs': MTRS, 'lines': LINES})

# ---- the left panel: a G-meter, or four readouts ------------------------------------------------------------------
W.append({'id': 'gmeter', 'type': 'gmeter', 'class': 'content', 'z': 2, 'x': 170, 'y': 170, 'w': 330, 'h': 330,
          'toggle': 'runwayLeft=gmeter'})
text('g_head', 185, 130, 300, 'w_label', 'G-FORCE', color='dim', toggle='runwayLeft=gmeter', spacing=2)
text('g_vals', 135, 515, 400, 'w_label', '{{gSide}}     {{gFwd}}', toggle='runwayLeft=gmeter')
text('g_best', 135, 548, 400, 'w_label', 'BEST {{gBest}} G', color='dim', toggle='runwayLeft=gmeter')
for i, (cx, cy) in enumerate([(230, 200), (440, 200), (230, 390), (440, 390)]):
    s = 'l%d' % (i + 1)
    text('l_head%d' % (i + 1), cx - 100, cy, 200, 'w_label', '{{slotHead:%s}}' % s, color='dim',
         toggle='runwayLeft=readouts', spacing=2)
    text('l_val%d' % (i + 1), cx - 100, cy + 40, 200, 'w_mid', '{{slot:%s}}' % s,
         toggle='runwayLeft=readouts')
    text('l_unit%d' % (i + 1), cx - 100, cy + 98, 200, 'w_label', '{{slotUnit:%s}}' % s, color='dim',
         toggle='runwayLeft=readouts')

# ---- the top bar: the range, what is playing ---------------------------------------------------------------------
W.append({'id': 'fuel_icon', 'type': 'icon', 'icon': 'fuel', 'z': 5, 'x': 640, 'y': 36, 'w': 26, 'h': 30, 'color': 'fg'})
text('range', 676, 34, 96, 'w_val', '{{range}}', align='right')
text('range_u', 778, 41, 44, 'w_label', '{{u:distLc}}', align='left')
text('media', 850, 32, 460, 'w_title', '{{mediaTitle}}', ellipsis=True, showWhen='media')
text('media_off', 850, 38, 460, 'w_label', '{{mode}}', color='dim', showWhen='!media', spacing=2)

# ---- between the bars: READY, the scale's unit, the gear, the drive mode, the speed -------------------------------
text('ready', 880, 102, 160, 'w_label', 'READY', spacing=1)
text('rpm_unit', 860, 130, 200, 'w_label', '1 / min x 1000', color='dim')
text('gear', 840, 292, 240, 'w_big', '{{gear}}', hotWhen='now')
text('mode', 855, 404, 210, 'w_label', '{{mode}}', spacing=1)
text('speed', 830, 446, 260, 'w_big', '{{speed}}')
text('speed_u', 900, 552, 120, 'w_label', '{{u:speedLc}}', color='dim')

# ---- the right panel: two rings -----------------------------------------------------------------------------------
for i, g in enumerate(RINGS):
    s = g['slot']
    text('ring_head%d' % (i + 1), g['cx'] - 110, g['cy'] - g['r'] - 70, 220, 'w_title', '{{slotTitle:%s}}' % s)
    text('ring_unit%d' % (i + 1), g['cx'] - 60, g['cy'] - 52, 120, 'w_label', '{{slotUnit:%s}}' % s)
    text('ring_val%d' % (i + 1), g['cx'] - 75, g['cy'] - 20, 150, 'w_mid', '{{slot:%s}}' % s)

# ---- the bottom row: the strip (BMW's gear letter at x 1380..1460 left uncovered, clear of the belt light) --------
W.append({'id': 'strip_cover_l', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 0, 'y': 660, 'w': 1380, 'h': 60,
          'color': 'bg', 'stripRow': 'l'})
W.append({'id': 'strip_cover_r', 'type': 'fill', 'class': 'content', 'z': 0, 'x': 1460, 'y': 660, 'w': 460, 'h': 60,
          'color': 'bg', 'stripRow': 'r'})
text('b1_head', 215, 674, 140, 'w_label', '{{slotHead:b1}}', color='dim', align='left', stripRow='l')
text('b1_val', 360, 672, 110, 'w_val', '{{slot:b1}}', align='right', stripRow='l')
text('b1_unit', 474, 680, 60, 'w_label', '{{slotUnit:b1}}', color='dim', align='left', stripRow='l')
text('time', 720, 672, 130, 'w_val', '{{time}}', align='right', stripRow='l')
text('ampm', 856, 680, 40, 'w_label', '{{ampmLc}}', color='dim', align='left', stripRow='l')
text('outside', 1060, 672, 110, 'w_val', '{{ambient}}', align='right', stripRow='l')
text('outside_u', 1174, 680, 40, 'w_label', '{{u:temp}}', color='dim', align='left', stripRow='l')
text('b2_min', 1480, 676, 60, 'w_label', 'MIN', color='dim', align='left', stripRow='r')
text('b2_head', 1545, 674, 160, 'w_label', '{{slotHead:b2}}', align='center', spacing=1, stripRow='r')
text('b2_max', 1710, 676, 60, 'w_label', 'MAX', color='dim', align='right', stripRow='r')

layout = {
    'schemaVersion': 2,
    'name': 'Runway',
    'packWaste': 6,
    'theme': 'runway',
    'slots': [
        {'id': 'r1', 'where': 'right, first ring', 'default': 'powerPct'},
        {'id': 'r2', 'where': 'right, second ring', 'default': 'torquePct'},
        {'id': 'b1', 'where': 'bottom left bar', 'default': 'coolant'},
        {'id': 'b2', 'where': 'bottom right bar', 'default': 'boost'},
        {'id': 'l1', 'where': 'left panel, top left', 'default': 'oil'},
        {'id': 'l2', 'where': 'left panel, top right', 'default': 'intake'},
        {'id': 'l3', 'where': 'left panel, bottom left', 'default': 'fuel'},
        {'id': 'l4', 'where': 'left panel, bottom right', 'default': 'gLat'},
    ],
    '_about': 'Runway cluster, generated by tools/gen_runway.py (edit that and regenerate): two rev bars leaning apart '
              'towards the driver like a runway, numbered per thousand, lit from the far end down to the revs and red past '
              'the redline; READY, the gear, the drive mode and the speed between them; two ring gauges on the right (power '
              'and torque out of the box); a G-meter on the left, or four readouts ("runwayLeft"); a top bar with the range '
              'and what is playing; a bottom row with two segmented bars (coolant and boost), the clock and the outside '
              'temperature. Every ring, bar and left readout is a readout slot. BMW\'s gear letter left uncovered. No map '
              'window. Widget reference: shared/hud.js header.',
    'widgets': W,
}

out = sys.argv[1] if len(sys.argv) > 1 else 'apps/cluster_themes/hud/layouts/runway.json'
with open(out, 'w') as f:
    json.dump(layout, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('%s: %d widgets' % (out, len(W)))
