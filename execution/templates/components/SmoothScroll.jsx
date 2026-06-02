"use client";

import { useEffect } from "react";
import Lenis from "lenis";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

/**
 * SmoothScroll component wraps the application pages and enables Lenis smooth scrolling
 * synchronized with GSAP ScrollTrigger.
 */
export default function SmoothScroll({ children }) {
  useEffect(() => {
    // Register GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // Initialize Lenis smooth scrolling
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      syncTouch: false,
    });

    // Update ScrollTrigger on Lenis scroll
    lenis.on("scroll", ScrollTrigger.update);

    // Connect GSAP ticker to Lenis requestAnimationFrame
    const updateRaf = (time) => {
      lenis.raf(time * 1000);
    };
    gsap.ticker.add(updateRaf);

    // Disable lag smoothing to prevent scroll jumping
    gsap.ticker.lagSmoothing(0);

    // Recalculate ScrollTrigger on window resize or DOM changes
    const resizeObserver = new ResizeObserver(() => {
      ScrollTrigger.refresh();
    });
    resizeObserver.observe(document.body);

    return () => {
      lenis.destroy();
      gsap.ticker.remove(updateRaf);
      resizeObserver.disconnect();
    };
  }, []);

  return <>{children}</>;
}
