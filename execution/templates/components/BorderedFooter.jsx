"use client";

import { motion } from "framer-motion";

export default function BorderedFooter({ title, subtitle, eyebrow }) {
  return (
    <footer className="relative w-full px-6 py-12 md:py-20 bg-background overflow-hidden border-t border-borderColor/80">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-8 relative z-10">
        <div>
          {eyebrow && (
            <span className="text-[10px] font-mono tracking-widest text-accent uppercase mb-2 block">
              {eyebrow}
            </span>
          )}
          
          <h3 className="text-lg md:text-xl font-header font-bold text-foreground mb-2">
            {title}
          </h3>
          
          <p className="text-xs font-body font-light text-foreground/45">
            {subtitle}
          </p>
        </div>

        <div className="flex gap-8 text-[10px] font-mono text-foreground/50">
          <a href="#" className="hover:text-accent transition-colors duration-300">CATALOGUE</a>
          <a href="#" className="hover:text-accent transition-colors duration-300">ARCHIVE</a>
          <a href="#" className="hover:text-accent transition-colors duration-300">CONTACT</a>
        </div>
      </div>

      <div className="max-w-7xl mx-auto border-t border-borderColor/40 mt-8 pt-6 flex justify-between items-center relative z-10 text-[9px] font-mono text-foreground/30">
        <span>
          © {new Date().getFullYear()} {eyebrow || "ANDIP"}. ALL EDITION INQUIRES PROTECTED.
        </span>
        
        <span>
          EDITION CODES: A3-CGN
        </span>
      </div>
    </footer>
  );
}
