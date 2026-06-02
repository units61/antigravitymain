# Directive: Next.js + TailwindCSS Code Generation SOP

## 1. Objective
This directive governs the Standard Operating Procedure (SOP) for the **Component Engine (Phase 3)**. It establishes rules for structuring, writing, styling, animating, and verifying the dynamically generated Next.js (App Router) + TailwindCSS applications.

---

## 2. Directory Structure of Generated App
The generated codebase must follow a strict, self-contained Next.js (App Router) layout:
```text
.tmp/builds/{session_id}/
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── hooks/
│   └── useGsapScroll.js
├── components/
│   ├── ImmersiveHero.jsx
│   ├── SplitSectionHero.jsx
│   ├── FeatureGrid.jsx
│   ├── AsymmetricFeatures.jsx
│   ├── InteractiveGallery.jsx
│   ├── ScrollRevealCards.jsx
│   ├── MotionCTA.jsx
│   ├── MinimalCTA.jsx
│   ├── GlassmorphicFooter.jsx
│   ├── BorderedFooter.jsx
│   ├── SmoothScroll.jsx
│   ├── Marquee.jsx
│   ├── BentoGrid.jsx
│   ├── ParallaxGallery.jsx
│   ├── MagneticButton.jsx
│   ├── TextReveal.jsx
│   ├── TestimonialCarousel.jsx
│   ├── StatsCounter.jsx
│   └── ScrollPinSection.jsx
└── app/
    ├── layout.js
    ├── page.js
    └── globals.css
```

---

## 3. Theming & Styling via CSS Variables
Dynamic styling tokens determined by the **Art Director** (Design DNA) must be bridged into TailwindCSS cleanly:
1. **Globals CSS Injection**: `theme_generator.py` will inject a custom `:root` block inside `app/globals.css`:
   ```css
   :root {
     --color-bg: #0D0D0D;
     --color-fg: #F5F5F0;
     --color-accent: #C5A880;
     --color-muted: #404040;
     --color-border: rgba(255,255,255,0.08);
     --color-card-bg: rgba(255,255,255,0.05);
     --border-radius: clamp(0.5rem, 1vw, 1rem);
     --border-width: 0.5px;
     --box-shadow: 0px 20px 50px rgba(0,0,0,0.25);
     --backdrop-blur: 12px;
     --font-header: 'Playfair Display', serif;
     --font-body: 'Inter', sans-serif;
   }
   ```
2. **Tailwind Mapping**: `tailwind.config.js` will map these variables dynamically:
   ```javascript
   module.exports = {
     content: [
       "./app/**/*.{js,ts,jsx,tsx}",
       "./components/**/*.{js,ts,jsx,tsx}",
     ],
     theme: {
       extend: {
         colors: {
           background: "var(--color-bg)",
           foreground: "var(--color-fg)",
           accent: "var(--color-accent)",
           muted: "var(--color-muted)",
           borderColor: "var(--color-border)",
           cardBg: "var(--color-card-bg)",
         },
         borderRadius: {
           custom: "var(--border-radius)",
         },
         borderWidth: {
           custom: "var(--border-width)",
         },
         backdropBlur: {
           custom: "var(--backdrop-blur)",
         },
         fontFamily: {
           header: "var(--font-header)",
           body: "var(--font-body)",
         }
       },
     },
     plugins: [],
   }
   ```

---

## 4. React Code & Animation Standards
All components written into the `components/` directory must adhere to premium frontend standards:
1. **Client Directives**: Every file using React hooks, standard state/effects, or Framer Motion animation triggers must prepend `"use client";` at the very first line.
2. **Motion Spring Configurations**: Read the `motion_config` properties (duration, damping, stiffness) from the component plan, translating them exactly:
   ```javascript
   import { motion } from "framer-motion";
   
   // In component:
   <motion.div
     initial={{ opacity: 0, y: 20 }}
     whileInView={{ opacity: 1, y: 0 }}
     viewport={{ once: true, margin: "-100px" }}
     transition={{
       type: "spring",
       stiffness: motionConfig.stiffness || 150,
       damping: motionConfig.damping || 12,
       duration: motionConfig.duration || 0.8
     }}
   >
     ...
   </motion.div>
   ```
3. **Accessibility (a11y)**:
   - Use semantic wrapper tags (`<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`).
   - Every active link or button element must have proper keyboard focus styles (e.g. `focus-visible:ring-2 focus-visible:ring-accent outline-none`).
   - Alt attributes for showcase/gallery images must be dynamically derived or populated using high-fidelity labels.
4. **GSAP & Lenis Integration Rules**:
   - Every GSAP animation tied to scrolling MUST use the `useGsapScroll` custom hook to guarantee memory safety and automatically call `ScrollTrigger.kill()` on unmount.
   - For all scroll-bound interactions (stagger reveals, parallax background blobs, splitting panel slide speed offset, horizontal scroll gallery sections, etc.), use GSAP ScrollTrigger `scrub: true` or `scrub: 1.2` for smooth, lag-free interpolation synced directly with the Lenis smooth scroll ticker.
5. **Embla Carousel React headless slider standards**:
   - Testimonial and showcase carousels should use `embla-carousel-react` as the slider frame, coupled with `embla-carousel-autoplay` if automatic sliding is required.
   - Ensure the carousel structure uses the standard Embla container, viewport, and slider tracks (`overflow-hidden` on viewport, `flex` on container, and `flex-[0_0_100%]` or `flex-[0_0_auto]` on individual slide elements) for responsive dragging/swiping.

---

## 5. Verification SOP
Before completing assembly:
1. **Folder Verification**: Check that all 3 configuration files, the standard stylesheets, and individual React files exist.
2. **Derivation Test**: Automatically verify that the generated codebase executes `npm run build` cleanly without syntax or linting errors.

---

## 6. ASLA YAPMA (Negative Constraints)
- **ASLA `"use client";` ifadesini unutup hydration hatalarına neden olma.** Framer Motion, GSAP, Lenis veya standard state/effect kullanan her React bileşeninin en üst satırına bu ifadeyi kesinlikle ekle.
- **ASLA TailwindCSS içinde `var(--color-bg)` gibi değişkenleri doğrudan sınıf isimleri yerine (`bg-[var(--color-bg)]` gibi) ham şekilde yazma.** Bunları `tailwind.config.js` içine map et ve `bg-background` veya `text-foreground` şeklinde çağır.
- **ASLA pürüzsüzleştirilmemiş scroll (ham window scroll) kullanan GSAP ScrollTrigger kodlama.** Lenis entegrasyonu her zaman aktif olmalı ve ScrollTrigger `scrub: 1` veya `scrub: 1.5` gibi akıcı değerlerle donatılmalıdır.
- **ASLA 3D WebGL katmanı üzerine gelen DOM metin kutularına `pointer-events: none` eklemeyi unutma.** Canvas altındaki 3D model etkileşimlerinin bloklanmaması için DOM yerleşim katmanlarında pointer event akışlarını kesinlikle kontrol et.
- **ASLA `ScrollTrigger.kill()` çağrısını yapmayan, cleanup edilmemiş ham GSAP useEffect blokları yazma.** Bellek sızıntılarını önlemek için GSAP animasyonlarını her zaman `useGsapScroll` kancası (hook) veya `gsap.context()` temizleme fonksiyonları ile sarmalla.
