(() => {
  const intro = document.querySelector('[data-game-intro]');
  const startButton = document.querySelector('[data-game-start]');
  const game = document.querySelector('[data-carpet-game]');
  const canvas = document.querySelector('#carpet-cleaning-game');
  if (!intro || !startButton || !game || !canvas) return;

  const context = canvas.getContext('2d');
  const stage = canvas.parentElement;
  const progressLabel = document.querySelector('[data-game-progress]');
  const progressBar = document.querySelector('[data-game-progress-bar]');
  const status = document.querySelector('[data-game-status]');
  const prize = document.querySelector('[data-game-prize]');
  const scrubber = new Image();
  scrubber.src = '/assets/scrub-brush.svg';

  let width = 1280;
  let height = 800;
  let spots = [];
  let confetti = [];
  let complete = false;
  let started = false;
  let animationFrame = 0;
  const pointer = { x: width * .72, y: height * .72, down: false, angle: 0 };

  const seededRandom = (() => {
    let seed = 404;
    return () => {
      seed = (seed * 9301 + 49297) % 233280;
      return seed / 233280;
    };
  })();

  const createSpots = () => Array.from({ length: Math.min(24, Math.max(18, Math.round(width * height / 56000))) }, (_, index) => ({
    x: 70 + seededRandom() * Math.max(1, width - 140),
    y: 70 + seededRandom() * Math.max(1, height - 140),
    radius: Math.max(25, Math.min(62, width * .04)) * (.7 + seededRandom() * .55),
    stretch: .65 + seededRandom() * .65,
    rotation: seededRandom() * Math.PI,
    dirt: 1,
    paw: index % 6 === 0,
  }));

  const drawCarpet = () => {
    const base = context.createLinearGradient(0, 0, width, height);
    base.addColorStop(0, '#ead8a8');
    base.addColorStop(.5, '#d8be83');
    base.addColorStop(1, '#efdcae');
    context.fillStyle = base;
    context.fillRect(0, 0, width, height);

    context.strokeStyle = '#7b2e42';
    context.lineWidth = Math.max(16, Math.min(28, width * .022));
    context.strokeRect(16, 16, width - 32, height - 32);
    context.strokeStyle = '#f2d789';
    context.lineWidth = 4;
    context.strokeRect(34, 34, width - 68, height - 68);

    context.save();
    context.globalAlpha = .28;
    context.strokeStyle = '#8c4a4e';
    context.lineWidth = 3;
    for (let y = 72; y < height - 52; y += 82) {
      for (let x = 74; x < width - 48; x += 94) {
        context.beginPath();
        context.moveTo(x, y - 24);
        context.lineTo(x + 32, y);
        context.lineTo(x, y + 24);
        context.lineTo(x - 32, y);
        context.closePath();
        context.stroke();
        context.beginPath();
        context.arc(x, y, 7, 0, Math.PI * 2);
        context.stroke();
      }
    }
    context.globalAlpha = .16;
    context.strokeStyle = '#fff8dd';
    context.lineWidth = 1;
    for (let y = 48; y < height - 34; y += 8) {
      context.beginPath();
      context.moveTo(32, y);
      context.quadraticCurveTo(width / 2, y + 5, width - 32, y);
      context.stroke();
    }
    context.restore();

    context.fillStyle = '#f5e3b0';
    for (let x = 26; x < width - 26; x += 18) {
      context.fillRect(x, 0, 7, 22);
      context.fillRect(x, height - 22, 7, 22);
    }
  };

  const drawPaw = (spot) => {
    context.save();
    context.translate(spot.x, spot.y);
    context.rotate(spot.rotation);
    context.scale(spot.stretch, 1);
    context.globalAlpha = spot.dirt * .68;
    context.fillStyle = '#624737';
    context.beginPath();
    context.ellipse(0, 10, spot.radius * .42, spot.radius * .34, 0, 0, Math.PI * 2);
    context.fill();
    [[-22,-20],[-7,-29],[11,-28],[26,-16]].forEach(([x,y]) => {
      context.beginPath();
      context.ellipse(x * spot.radius / 55, y * spot.radius / 55, spot.radius * .12, spot.radius * .17, 0, 0, Math.PI * 2);
      context.fill();
    });
    context.restore();
  };

  const drawDirt = (spot) => {
    if (spot.dirt <= .01) return;
    if (spot.paw) {
      drawPaw(spot);
      return;
    }
    context.save();
    context.translate(spot.x, spot.y);
    context.rotate(spot.rotation);
    context.scale(spot.stretch, 1);
    context.globalAlpha = spot.dirt;
    const mud = context.createRadialGradient(0, 0, 2, 0, 0, spot.radius);
    mud.addColorStop(0, 'rgba(72,51,36,.82)');
    mud.addColorStop(.58, 'rgba(95,67,43,.62)');
    mud.addColorStop(1, 'rgba(85,57,37,0)');
    context.fillStyle = mud;
    context.beginPath();
    context.arc(0, 0, spot.radius, 0, Math.PI * 2);
    context.fill();
    context.fillStyle = 'rgba(69,47,32,.42)';
    [[.72,-.2],[-.68,.25],[.35,.7],[-.3,-.78]].forEach(([x,y], index) => {
      context.beginPath();
      context.arc(x * spot.radius, y * spot.radius, spot.radius * (.08 + index * .012), 0, Math.PI * 2);
      context.fill();
    });
    context.restore();
  };

  const drawScrubber = () => {
    if (!scrubber.complete || !scrubber.naturalWidth) return;
    const brushWidth = Math.max(94, Math.min(142, width * .12));
    const brushHeight = brushWidth * 236.1 / 558.47;
    context.save();
    context.translate(pointer.x, pointer.y);
    context.rotate(pointer.angle);
    context.shadowColor = 'rgba(7,19,31,.34)';
    context.shadowBlur = pointer.down ? 10 : 7;
    context.shadowOffsetY = 5;
    context.drawImage(scrubber, -brushWidth / 2, -brushHeight / 2, brushWidth, brushHeight);
    context.restore();
  };

  const drawConfetti = () => {
    confetti.forEach((piece) => {
      context.save();
      context.translate(piece.x, piece.y);
      context.rotate(piece.spin);
      context.fillStyle = piece.color;
      context.fillRect(-5, -3, 10, 6);
      context.restore();
      piece.x += piece.vx;
      piece.y += piece.vy;
      piece.vy += .08;
      piece.spin += piece.rotation;
    });
    confetti = confetti.filter((piece) => piece.y < height + 25);
  };

  const render = () => {
    cancelAnimationFrame(animationFrame);
    drawCarpet();
    spots.forEach(drawDirt);
    drawScrubber();
    drawConfetti();
    if (confetti.length) animationFrame = requestAnimationFrame(render);
  };

  const progress = () => Math.round((1 - spots.reduce((sum, spot) => sum + spot.dirt, 0) / spots.length) * 100);

  const celebrate = () => {
    complete = true;
    prize.hidden = false;
    status.textContent = 'Carpet rescued. Your reward is ready.';
    const colors = ['#48ca6d','#fff0a6','#ffffff','#f06a78','#7ed9df'];
    confetti = Array.from({ length: 90 }, () => ({
      x: width * .5 + (Math.random() - .5) * Math.min(300, width * .5),
      y: height * .42 + (Math.random() - .5) * 80,
      vx: (Math.random() - .5) * 6,
      vy: -2 - Math.random() * 6,
      spin: Math.random() * Math.PI,
      rotation: (Math.random() - .5) * .3,
      color: colors[Math.floor(Math.random() * colors.length)],
    }));
  };

  const updateProgress = () => {
    const value = Math.min(100, progress());
    progressLabel.textContent = `${value}%`;
    progressBar.style.width = `${value}%`;
    if (!complete && spots.every((spot) => spot.dirt <= .01)) celebrate();
  };

  const cleanAt = (x, y, strength = .28) => {
    if (complete) return;
    const brushReach = Math.max(52, Math.min(82, width * .065));
    spots.forEach((spot) => {
      const reach = spot.radius + brushReach;
      const distance = Math.hypot(x - spot.x, y - spot.y);
      if (distance < reach) {
        const force = Math.max(.12, 1 - distance / reach);
        spot.dirt = Math.max(0, spot.dirt - strength * force);
      }
    });
    updateProgress();
    render();
  };

  const canvasPoint = (event) => {
    const rect = canvas.getBoundingClientRect();
    return { x: event.clientX - rect.left, y: event.clientY - rect.top };
  };

  const movePointer = (point) => {
    const deltaX = point.x - pointer.x;
    pointer.angle += (Math.max(-.24, Math.min(.24, deltaX / 180)) - pointer.angle) * .45;
    pointer.x = Math.max(35, Math.min(width - 35, point.x));
    pointer.y = Math.max(28, Math.min(height - 28, point.y));
  };

  canvas.addEventListener('pointerdown', (event) => {
    canvas.setPointerCapture(event.pointerId);
    pointer.down = true;
    movePointer(canvasPoint(event));
    cleanAt(pointer.x, pointer.y, 1);
  });
  canvas.addEventListener('pointermove', (event) => {
    if (!pointer.down) return;
    movePointer(canvasPoint(event));
    cleanAt(pointer.x, pointer.y, .85);
  });
  const endPointer = () => {
    pointer.down = false;
    pointer.angle *= .5;
    render();
  };
  canvas.addEventListener('pointerup', endPointer);
  canvas.addEventListener('pointercancel', endPointer);

  canvas.addEventListener('keydown', (event) => {
    const move = event.shiftKey ? 34 : 19;
    const directions = {
      ArrowLeft: [-move, 0], ArrowRight: [move, 0],
      ArrowUp: [0, -move], ArrowDown: [0, move],
    };
    if (directions[event.key]) {
      event.preventDefault();
      movePointer({ x: pointer.x + directions[event.key][0], y: pointer.y + directions[event.key][1] });
      cleanAt(pointer.x, pointer.y, .55);
    } else if (event.key === ' ' || event.key === 'Enter') {
      event.preventDefault();
      cleanAt(pointer.x, pointer.y, .52);
    }
  });

  const resizeCanvas = () => {
    if (!started) return;
    const oldWidth = width;
    const oldHeight = height;
    const rect = stage.getBoundingClientRect();
    width = Math.max(320, rect.width);
    height = Math.max(320, rect.height);
    const density = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = Math.round(width * density);
    canvas.height = Math.round(height * density);
    context.setTransform(density, 0, 0, density, 0, 0);
    if (spots.length) {
      spots.forEach((spot) => {
        spot.x *= width / oldWidth;
        spot.y *= height / oldHeight;
      });
      pointer.x *= width / oldWidth;
      pointer.y *= height / oldHeight;
    }
    render();
  };

  const beginGame = () => {
    intro.hidden = true;
    game.hidden = false;
    document.body.classList.add('game-active');
    started = true;
    resizeCanvas();
    spots = createSpots();
    pointer.x = width * .72;
    pointer.y = height * .72;
    pointer.angle = 0;
    prize.hidden = true;
    updateProgress();
    render();
    canvas.focus({ preventScroll: true });
    const root = document.documentElement;
    const previousScrollBehavior = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto';
    const resetPagePosition = () => {
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
      document.scrollingElement.scrollTop = 0;
    };
    requestAnimationFrame(() => {
      resetPagePosition();
      requestAnimationFrame(() => {
        resetPagePosition();
        root.style.scrollBehavior = previousScrollBehavior;
      });
    });
  };

  scrubber.addEventListener('load', render);
  startButton.addEventListener('click', beginGame);
  window.addEventListener('resize', resizeCanvas);
})();
