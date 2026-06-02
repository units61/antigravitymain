"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

export default function MotionCTA({ title, subtitle, eyebrow, primary_cta, motion_config }) {
  const transition = {
    type: "spring",
    stiffness: motion_config?.stiffness || 120,
    damping: motion_config?.damping || 14,
    duration: motion_config?.duration || 1.2,
  };

  return (
    <section className="relative py-24 md:py-36 px-6 bg-background overflow-hidden flex flex-col justify-center items-center text-center">
      {/* Dynamic Background Glows */}
      <div className="absolute inset-0 z-0 pointer-events-none opacity-10">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] rounded-full bg-accent filter blur-[150px]" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto flex flex-col items-center">
        {eyebrow && (
          <motion.span
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ ...transition, delay: 0.1 }}
            className="text-xs uppercase tracking-[0.3em] font-semibold text-accent mb-4 block"
          >
            {eyebrow}
          </motion.span>
        )}

        <motion.h2
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ ...transition, delay: 0.2 }}
          className="text-4xl md:text-6xl font-header font-bold tracking-tight text-foreground leading-tight mb-6"
        >
          {title}
        </motion.h2>

        {subtitle && (
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ ...transition, delay: 0.4 }}
            className="text-base md:text-xl font-body font-light text-foreground/75 max-w-xl mb-10 leading-relaxed"
          >
            {subtitle}
          </motion.p>
        )}

        {primary_cta && primary_cta.text && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ ...transition, delay: 0.5 }}
          >
            <button
              onClick={() => {
                alert(`Triggered action: ${primary_cta.action}`);
              }}
              className="group relative flex items-center gap-3 px-10 py-5 rounded-custom bg-accent text-background font-body font-bold tracking-wider hover:shadow-[0_0_40px_var(--color-accent)] transition-all duration-300 transform active:scale-95 outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              <span>{primary_cta.text}</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
            </button>
          </motion.div>
        )}
      </div>

      <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-borderColor to-transparent" />
    </section>
  );
}
