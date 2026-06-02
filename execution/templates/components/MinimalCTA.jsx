"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

export default function MinimalCTA({ title, subtitle, eyebrow, primary_cta, motion_config }) {
  const transition = {
    type: "spring",
    stiffness: motion_config?.stiffness || 150,
    damping: motion_config?.damping || 15,
  };

  return (
    <section className="relative py-20 md:py-28 px-6 bg-background overflow-hidden border-t border-borderColor/60">
      <div className="max-w-5xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-8 md:gap-12">
        <div className="max-w-xl">
          {eyebrow && (
            <span className="text-[10px] uppercase tracking-[0.3em] font-semibold text-accent mb-3 block">
              {eyebrow}
            </span>
          )}
          
          <motion.h2
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={transition}
            className="text-3xl md:text-4xl font-header font-bold text-foreground mb-4 leading-snug"
          >
            {title}
          </motion.h2>

          {subtitle && (
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={transition}
              className="text-sm md:text-base font-body font-light text-foreground/60 leading-relaxed"
            >
              {subtitle}
            </motion.p>
          )}
        </div>

        {primary_cta && primary_cta.text && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={transition}
            className="flex-shrink-0"
          >
            <button
              onClick={() => {
                alert(`Triggered action: ${primary_cta.action}`);
              }}
              className="group flex items-center gap-3 px-8 py-4 rounded-custom bg-transparent border border-borderColor hover:border-accent hover:text-accent font-body font-semibold tracking-wide transition-all duration-300 transform active:scale-95 outline-none focus-visible:ring-2 focus-visible:ring-accent"
            >
              <span>{primary_cta.text}</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
            </button>
          </motion.div>
        )}
      </div>
    </section>
  );
}
