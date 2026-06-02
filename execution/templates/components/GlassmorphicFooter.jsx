"use client";

import { motion } from "framer-motion";

export default function GlassmorphicFooter({ title, subtitle, eyebrow }) {
  return (
    <footer className="relative w-full px-6 py-16 md:py-24 bg-background overflow-hidden border-t border-borderColor/50">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-12 relative z-10">
        
        {/* Left branding segment */}
        <div className="max-w-md">
          {eyebrow && (
            <span className="text-xs uppercase tracking-[0.3em] font-bold text-accent mb-3 block">
              {eyebrow}
            </span>
          )}
          
          <h3 className="text-xl md:text-3xl font-header font-bold text-foreground mb-4">
            {title}
          </h3>
          
          <p className="text-xs md:text-sm font-body font-light text-foreground/50 leading-relaxed">
            {subtitle}
          </p>
        </div>

        {/* Right Links segment */}
        <div className="flex flex-wrap gap-8 md:gap-16">
          <div className="flex flex-col gap-3">
            <span className="text-[10px] font-mono tracking-widest text-accent uppercase mb-2">// INITIATIVES</span>
            <a href="#" className="text-xs md:text-sm font-body text-foreground/60 hover:text-accent transition-colors duration-300">The Rebellion</a>
            <a href="#" className="text-xs md:text-sm font-body text-foreground/60 hover:text-accent transition-colors duration-300">Bespoke Design</a>
            <a href="#" className="text-xs md:text-sm font-body text-foreground/60 hover:text-accent transition-colors duration-300">Limited Droppings</a>
          </div>
          
          <div className="flex flex-col gap-3">
            <span className="text-[10px] font-mono tracking-widest text-accent uppercase mb-2">// CONNECTION</span>
            <a href="#" className="text-xs md:text-sm font-body text-foreground/60 hover:text-accent transition-colors duration-300">Instagram</a>
            <a href="#" className="text-xs md:text-sm font-body text-foreground/60 hover:text-accent transition-colors duration-300">Twitter X</a>
            <a href="#" className="text-xs md:text-sm font-body text-foreground/60 hover:text-accent transition-colors duration-300">Discord Collective</a>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto border-t border-borderColor/40 mt-12 md:mt-16 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 relative z-10">
        <span className="text-[10px] font-mono text-foreground/40">
          © {new Date().getFullYear()} {eyebrow || "ANDIP"}. ALL RIGHTS RESERVED. HANDCRAFTED VIA COMPONENT ENGINE.
        </span>
        
        <div className="flex gap-6 text-[10px] font-mono text-foreground/40">
          <a href="#" className="hover:text-accent transition-colors">PRIVACY CODE</a>
          <a href="#" className="hover:text-accent transition-colors">TERMS OF USE</a>
        </div>
      </div>
    </footer>
  );
}
