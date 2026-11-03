import json, base64, re

def main():
    # 1. Read base64 webp
    with open('princess_atlas.webp', 'rb') as f:
        b64_webp = base64.b64encode(f.read()).decode('utf-8')

    # 2. Read index.html
    with open('index.html', 'r') as f:
        content = f.read()

    # 3. Frames for princess and dipkiss
    img_data = {
      'idle_0': {'x': 265, 'y': 60, 'w': 67, 'h': 82, 'ox': 33.5, 'oy': 82.0},
      'idle_1': {'x': 344, 'y': 60, 'w': 62, 'h': 82, 'ox': 31.0, 'oy': 82.0},
      'idle_2': {'x': 418, 'y': 60, 'w': 61, 'h': 82, 'ox': 30.5, 'oy': 82.0},
      'idle_3': {'x': 489, 'y': 60, 'w': 71, 'h': 82, 'ox': 35.5, 'oy': 82.0},
      
      'run_0': {'x': 595, 'y': 60, 'w': 79, 'h': 82, 'ox': 39.5, 'oy': 82.0},
      'run_1': {'x': 684, 'y': 60, 'w': 90, 'h': 82, 'ox': 45.0, 'oy': 82.0},
      'run_2': {'x': 782, 'y': 60, 'w': 77, 'h': 82, 'ox': 38.5, 'oy': 82.0},
      'run_3': {'x': 868, 'y': 60, 'w': 67, 'h': 82, 'ox': 33.5, 'oy': 82.0},
      'run_4': {'x': 941, 'y': 60, 'w': 64, 'h': 82, 'ox': 32.0, 'oy': 82.0},
      
      'jump_0': {'x': 251, 'y': 187, 'w': 66, 'h': 88, 'ox': 33.0, 'oy': 88.0},
      'jump_1': {'x': 332, 'y': 187, 'w': 65, 'h': 88, 'ox': 32.5, 'oy': 88.0},
      'jump_2': {'x': 419, 'y': 187, 'w': 51, 'h': 88, 'ox': 25.5, 'oy': 88.0},
      'jump_3': {'x': 485, 'y': 187, 'w': 64, 'h': 88, 'ox': 32.0, 'oy': 88.0},
      
      'fall_0': {'x': 605, 'y': 187, 'w': 64, 'h': 88, 'ox': 32.0, 'oy': 88.0},
      'fall_1': {'x': 694, 'y': 187, 'w': 76, 'h': 88, 'ox': 38.0, 'oy': 88.0},
      'fall_2': {'x': 804, 'y': 187, 'w': 61, 'h': 88, 'ox': 30.5, 'oy': 88.0},
      'fall_3': {'x': 900, 'y': 218, 'w': 75, 'h': 57, 'ox': 37.5, 'oy': 57.0},
      
      'walk_0': {'x': 16, 'y': 315, 'w': 60, 'h': 83, 'ox': 30.0, 'oy': 83.0},
      'walk_1': {'x': 94, 'y': 315, 'w': 54, 'h': 83, 'ox': 27.0, 'oy': 83.0},
      'walk_2': {'x': 167, 'y': 315, 'w': 58, 'h': 83, 'ox': 29.0, 'oy': 83.0},
      'walk_3': {'x': 248, 'y': 315, 'w': 55, 'h': 83, 'ox': 27.5, 'oy': 83.0},
      'walk_4': {'x': 325, 'y': 315, 'w': 56, 'h': 83, 'ox': 28.0, 'oy': 83.0},
      
      'magic_0': {'x': 423, 'y': 315, 'w': 75, 'h': 83, 'ox': 37.5, 'oy': 83.0},
      'magic_1': {'x': 499, 'y': 315, 'w': 105, 'h': 83, 'ox': 52.5, 'oy': 83.0},
      'magic_2': {'x': 605, 'y': 315, 'w': 85, 'h': 83, 'ox': 42.5, 'oy': 83.0},
      
      'dash_0': {'x': 714, 'y': 315, 'w': 109, 'h': 83, 'ox': 54.5, 'oy': 83.0},
      'dash_1': {'x': 835, 'y': 315, 'w': 111, 'h': 83, 'ox': 55.5, 'oy': 83.0},
      
      'hurt_0': {'x': 15, 'y': 445, 'w': 60, 'h': 84, 'ox': 30.0, 'oy': 84.0},
      'hurt_1': {'x': 107, 'y': 445, 'w': 59, 'h': 84, 'ox': 29.5, 'oy': 84.0},
      'hurt_2': {'x': 194, 'y': 445, 'w': 63, 'h': 84, 'ox': 31.5, 'oy': 84.0},
      
      'death_0': {'x': 311, 'y': 445, 'w': 69, 'h': 84, 'ox': 34.5, 'oy': 84.0},
      'death_1': {'x': 401, 'y': 445, 'w': 60, 'h': 84, 'ox': 30.0, 'oy': 84.0},
      'death_2': {'x': 487, 'y': 475, 'w': 92, 'h': 54, 'ox': 46.0, 'oy': 54.0},
      'death_3': {'x': 618, 'y': 485, 'w': 85, 'h': 44, 'ox': 42.5, 'oy': 44.0},
      
      'special_0': {'x': 757, 'y': 445, 'w': 251, 'h': 115, 'ox': 125.5, 'oy': 115.0},
      'portrait': {'x': 20, 'y': 50, 'w': 185, 'h': 190, 'ox': 92.5, 'oy': 190.0}
    }

    dipkiss_data = {
      'dipkiss_0': {'x': 26, 'y': 586, 'w': 115, 'h': 78, 'ox': 63.0, 'oy': 78.0},
      'dipkiss_1': {'x': 166, 'y': 586, 'w': 88, 'h': 78, 'ox': 47.0, 'oy': 78.0},
      'dipkiss_2': {'x': 269, 'y': 586, 'w': 80, 'h': 78, 'ox': 44.0, 'oy': 78.0},
      'dipkiss_3': {'x': 373, 'y': 586, 'w': 87, 'h': 78, 'ox': 46.0, 'oy': 78.0},
      'dipkiss_4': {'x': 485, 'y': 586, 'w': 115, 'h': 78, 'ox': 56.0, 'oy': 78.0},
      'dipkiss_5': {'x': 624, 'y': 574, 'w': 118, 'h': 90, 'ox': 63.0, 'oy': 90.0},
      'dipkiss_6': {'x': 765, 'y': 586, 'w': 114, 'h': 78, 'ox': 64.0, 'oy': 78.0}
    }

    # 4. Update ATLAS_DATA
    idx_start = content.find('ATLAS_DATA = ') + len('ATLAS_DATA = ')
    idx_end = content.find(';\n', idx_start)
    atlas = json.loads(content[idx_start:idx_end])
    atlas['princess'] = img_data
    atlas['dipkiss'] = dipkiss_data

    new_atlas_json = json.dumps(atlas)
    content = content[:idx_start] + new_atlas_json + content[idx_end:]

    # 5. Update PRINCESS_IMG loader
    p_match = re.search(r'const PRINCESS_IMG = new Image\(\);\s+PRINCESS_IMG\.src = "[^"]+";', content)
    if p_match:
        replacement = 'const PRINCESS_IMG = new Image();\n  PRINCESS_IMG.src = "data:image/webp;base64,' + b64_webp + '";\n  try {\n    const localPrincess = new Image();\n    localPrincess.onload = function () {\n      PRINCESS_IMG.src = localPrincess.src;\n    };\n    localPrincess.src = "princess_atlas.png";\n  } catch (e) {}'
        content = content[:p_match.start()] + replacement + content[p_match.end():]
        print('Updated PRINCESS_IMG loader successfully.')
    else:
        print('WARNING: Could not find PRINCESS_IMG regex!')

    # 6. Update drawPrincess and add drawDipKiss
    draw_princess_code = '''  function drawPrincess(pr, camX) {
    if (!pr.active) return;
    if (state === 'ending' && endingPhase === 'kiss') return;
    var x = Math.round(pr.x - camX), y = Math.round(pr.y);
    var frName = 'idle_0';

    if (endingPhase === 'kiss') {
      frName = 'idle_0';
    } else if (Math.abs(pr.vx) > 10 || (state === 'ending' && endingPhase === 'reunion' && pr.x > 3390)) {
      var wIdx = Math.floor(t * 6) % 5;
      frName = 'walk_' + wIdx;
    } else {
      var iIdx = Math.floor(pr.anim * 3.5) % 4;
      frName = 'idle_' + iIdx;
    }

    var fr = (ATLAS_DATA.princess && ATLAS_DATA.princess[frName]) || (ATLAS_DATA.princess && ATLAS_DATA.princess['idle_0']);
    var SCALE = 0.44;

    ctx.save();
    ctx.translate(x + Math.round(pr.w / 2), y + pr.h);
    ctx.scale(pr.face, 1);

    ctx.shadowColor = '#34d399';
    ctx.shadowBlur = 8 + Math.sin(t * 5) * 3;

    if (fr && PRINCESS_IMG.complete) {
      ctx.drawImage(
        PRINCESS_IMG,
        fr.x, fr.y, fr.w, fr.h,
        Math.round(-fr.ox * SCALE),
        Math.round(-fr.oy * SCALE),
        Math.round(fr.w * SCALE),
        Math.round(fr.h * SCALE)
      );
    }

    // Floating Emerald reunion particles
    if (Math.random() < 0.35) {
      parts.push({
        x: pr.x + pr.w / 2 + rnd(-12, 12),
        y: pr.y + rnd(0, pr.h),
        vx: rnd(-10, 10),
        vy: rnd(-25, -10),
        life: 0.6,
        max: 0.6,
        c: Math.random() < 0.5 ? '#34d399' : '#a7f3d0',
        s: rnd(1.5, 3),
        g: -10
      });
    }

    ctx.restore();
  }

  function drawDipKiss(camX) {
    var cx = Math.round(3378 - camX);
    var cy = GROUND_Y;
    var kProg = clamp((endingTimer - 4.5) / 3.8, 0, 0.999);

    // 7 sequential animation frames across 4.0s kiss duration
    // Frame 0: 0.00 - 0.12 (Take hands / approach)
    // Frame 1: 0.12 - 0.25 (Draw close / eye contact)
    // Frame 2: 0.25 - 0.38 (Lovers embrace tightly)
    // Frame 3: 0.38 - 0.50 (Begin graceful dip arch)
    // Frame 4: 0.50 - 0.64 (Deep dip back)
    // Frame 5: 0.64 - 0.88 (CLIMAX DIP KISS with floating heart!)
    // Frame 6: 0.88 - 1.00 (Lift up gently from dip, holding tenderly)
    var frameIdx = 0;
    if (kProg < 0.12) frameIdx = 0;
    else if (kProg < 0.25) frameIdx = 1;
    else if (kProg < 0.38) frameIdx = 2;
    else if (kProg < 0.50) frameIdx = 3;
    else if (kProg < 0.64) frameIdx = 4;
    else if (kProg < 0.88) frameIdx = 5;
    else frameIdx = 6;

    var fr = (ATLAS_DATA.dipkiss && ATLAS_DATA.dipkiss['dipkiss_' + frameIdx]) || (ATLAS_DATA.dipkiss && ATLAS_DATA.dipkiss['dipkiss_0']);
    var SCALE = 0.46;

    ctx.save();

    // 1. Radiant romantic dawn background aura
    var auraPulse = Math.sin(t * 3.5) * 8;
    var auraGrad = ctx.createRadialGradient(cx, cy - 28, 6, cx, cy - 28, 65 + auraPulse);
    auraGrad.addColorStop(0, 'rgba(255, 99, 132, 0.38)');
    auraGrad.addColorStop(0.35, 'rgba(52, 211, 153, 0.24)');
    auraGrad.addColorStop(0.70, 'rgba(251, 191, 36, 0.14)');
    auraGrad.addColorStop(1, 'rgba(16, 185, 129, 0)');
    ctx.fillStyle = auraGrad;
    ctx.fillRect(cx - 80, cy - 90, 160, 100);

    // 2. Soft ground shadow beneath lovers
    ctx.fillStyle = 'rgba(12, 6, 20, 0.42)';
    ctx.beginPath();
    ctx.ellipse(cx, cy - 1, 26, 4, 0, 0, Math.PI * 2);
    ctx.fill();

    // 3. Render authentic 7-frame pixel-art dip kiss sprite
    if (fr && PRINCESS_IMG.complete) {
      ctx.shadowColor = (frameIdx === 5) ? '#ff4d66' : '#34d399';
      ctx.shadowBlur = (frameIdx === 5) ? 14 : 8;
      ctx.drawImage(
        PRINCESS_IMG,
        fr.x, fr.y, fr.w, fr.h,
        Math.round(cx - fr.ox * SCALE),
        Math.round(cy - fr.oy * SCALE),
        Math.round(fr.w * SCALE),
        Math.round(fr.h * SCALE)
      );
    }

    // 4. Floating romantic petals, golden stardust, and heart sparkles
    for (var pi = 0; pi < 14; pi++) {
      var px = cx + Math.sin(t * 2 + pi * 1.6) * 36 + ((pi * 23) % 40) - 20;
      var py = cy - 14 - ((t * 22 + pi * 19) % 72);
      if (pi % 4 === 0) {
        drawHeartGem(Math.round(px - 4), Math.round(py - 4), true);
      } else if (pi % 2 === 0) {
        R(Math.round(px), Math.round(py), 3, 2, (pi % 6 === 0) ? '#ff4d66' : '#fb7185');
      } else {
        R(Math.round(px), Math.round(py), 2, 2, '#ffffff');
        R(Math.round(px - 1), Math.round(py), 4, 1, '#fde047');
        R(Math.round(px), Math.round(py - 1), 1, 4, '#fde047');
      }
    }

    // Climax Heart Glow on Frame 5
    if (frameIdx === 5) {
      var hx = cx + Math.round(8 * SCALE);
      var hy = cy - Math.round(fr.oy * SCALE) + 4;
      ctx.save();
      ctx.shadowColor = '#ff2a55';
      ctx.shadowBlur = 16;
      drawHeartGem(hx - 4, hy - 4, true);
      ctx.restore();
    }

    ctx.restore();
  }'''

    dp_match = re.search(r'  function drawPrincess\(pr, camX\) \{.*?\n  \}\n\n  function drawBossDefeat', content, re.DOTALL)
    if dp_match:
        content = content[:dp_match.start()] + draw_princess_code + '\n\n  function drawBossDefeat' + content[dp_match.end():]
        print('Updated drawPrincess and added drawDipKiss successfully.')
    else:
        print('WARNING: Could not find drawPrincess match!')

    # 7. Update reunion dialog in drawHUD to show Riya portrait
    reunion_old = '''      if (endingPhase === 'reunion') {
        if (endingTimer >= 1.5 && endingTimer < 3.2) {
          R(W / 2 - 140, 48, 280, 40, 'rgba(16, 28, 20, 0.88)');
          R(W / 2 - 140, 48, 280, 2, '#34d399');
          txt('RIYA', W / 2 - 130, 52, '#34d399', 8, 'left');
          txt('"You came back..."', W / 2 - 130, 68, '#ffffff', 8, 'left');
        } else if (endingTimer >= 3.2 && endingTimer < 4.5) {
          R(W / 2 - 140, 48, 280, 40, 'rgba(28, 16, 20, 0.88)');
          R(W / 2 - 140, 48, 280, 2, '#ff4d66');
          txt('NAKS', W / 2 - 130, 52, '#ff4d66', 8, 'left');
          txt('"I promised I would."', W / 2 - 130, 68, '#ffffff', 8, 'left');
        }
      }'''

    reunion_new = '''      if (endingPhase === 'reunion') {
        if (endingTimer >= 1.5 && endingTimer < 3.2) {
          R(W / 2 - 140, 44, 280, 44, 'rgba(12, 24, 16, 0.92)');
          R(W / 2 - 140, 44, 280, 2, '#34d399');
          var pFr = ATLAS_DATA.princess && ATLAS_DATA.princess['portrait'];
          if (pFr && PRINCESS_IMG.complete) {
            ctx.save();
            ctx.drawImage(PRINCESS_IMG, pFr.x, pFr.y, pFr.w, pFr.h, W / 2 - 134, 48, 36, 36);
            ctx.restore();
            txt('RIYA', W / 2 - 90, 52, '#34d399', 8, 'left');
            txt('"You came back..."', W / 2 - 90, 68, '#ffffff', 8, 'left');
          } else {
            txt('RIYA', W / 2 - 130, 52, '#34d399', 8, 'left');
            txt('"You came back..."', W / 2 - 130, 68, '#ffffff', 8, 'left');
          }
        } else if (endingTimer >= 3.2 && endingTimer < 4.5) {
          R(W / 2 - 140, 44, 280, 44, 'rgba(28, 14, 18, 0.92)');
          R(W / 2 - 140, 44, 280, 2, '#ff4d66');
          txt('NAKS', W / 2 - 130, 52, '#ff4d66', 8, 'left');
          txt('"I promised I would."', W / 2 - 130, 68, '#ffffff', 8, 'left');
        }
      }'''

    if reunion_old in content:
        content = content.replace(reunion_old, reunion_new)
        print('Updated reunion dialog with Riya portrait.')
    else:
        print('reunion_old exact match not found, looking for alternative...')

    # 8. Write to index.html and Ashen Vale.html
    with open('index.html', 'w') as f:
        f.write(content)
    with open('Ashen Vale.html', 'w') as f:
        f.write(content)

    print('Successfully written index.html and Ashen Vale.html!')

if __name__ == '__main__':
    main()

