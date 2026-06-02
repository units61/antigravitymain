"use client";

import { useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

/**
 * useGsapScroll Hook
 * 
 * A reusable hook to easily bind GSAP animations to scrolling using ScrollTrigger.
 * Runs once on mount to avoid re-initialization loops from dynamic option structures.
 * 
 * @param {React.RefObject} targetRef - The React Ref of the element to trigger or animate.
 * @param {Object} options - ScrollTrigger configuration options.
 * @param {Function} [options.animate] - A callback function that takes the element and returns a GSAP animation/timeline.
 * @param {string|Element} [options.trigger] - The element that triggers the scroll action. Defaults to targetRef.current.
 * @param {string} [options.start] - Start position of ScrollTrigger. Defaults to "top bottom".
 * @param {string} [options.end] - End position of ScrollTrigger. Defaults to "bottom top".
 * @param {boolean|number} [options.scrub] - Link scroll position to animation progress. Defaults to true.
 * @param {boolean} [options.pin] - Pin the trigger element during scroll. Defaults to false.
 */
export default function useGsapScroll(targetRef, options = {}) {
  useEffect(() => {
    if (!targetRef.current) return;

    // Register ScrollTrigger plugin
    gsap.registerPlugin(ScrollTrigger);
    
    const element = targetRef.current;
    
    let {
      animate,
      trigger = element,
      start = "top bottom",
      end = "bottom top",
      scrub = true,
      pin = false,
      markers = false,
      ...rest
    } = options;

    // Auto-unwrap React ref if passed as trigger option
    if (trigger && typeof trigger === "object" && "current" in trigger) {
      trigger = trigger.current;
    }

    let animInstance;
    
    // If an animate callback is provided, invoke it to build the GSAP animation
    if (animate && typeof animate === "function") {
      animInstance = animate(element);
    }

    // Create the ScrollTrigger instance
    const triggerInstance = ScrollTrigger.create({
      trigger,
      start,
      end,
      scrub,
      pin,
      markers,
      animation: animInstance,
      ...rest
    });

    // Cleanup on unmount
    return () => {
      if (triggerInstance) triggerInstance.kill();
      if (animInstance) animInstance.kill();
    };
  }, []);
}
