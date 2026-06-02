"use client";

import { motion } from "framer-motion";

export default function AsymmetricFeatures({ title, subtitle, items, motion_config }) {
  const transition = {
    type: "spring",
    stiffness: motion_config?.stiffness || 100,
    damping: motion_config?.damping || 15,
    duration: motion_config?.duration || 0.8,
  };

  return (
    <section className="relative py-24 md:py-32 px-6 bg-background overflow-hidden">
      <div className="max-w-7xl mx-auto">
        {/* Header Block */}
        <div className="mb-20 md:mb-28 max-w-2xl">
          <motion.h2
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
            className="text-3xl md:text-5xl font-header font-bold text-foreground mb-6"
          >
            {title}
          </motion.h2>
          
          {subtitle && (
            <motion.p
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-base md:text-lg font-body font-light text-foreground/60 leading-relaxed"
            >
              {subtitle}
            </motion.p>
          )}
        </div>

        {/* Asymmetric Alternating Layout */}
        {items && items.length > 0 && (
          <div className="flex flex-col gap-24 md:gap-32">
            {items.map((item, index) => {
              const isEven = index % 2 === 0;
              return (
                <div
                  key={index}
                  className={`flex flex-col ${isEven ? "md:flex-row" : "md:flex-row-reverse"} gap-8 md:gap-16 items-center`}
                >
                  {/* Copy Area */}
                  <motion.div
                    initial={{ opacity: 0, x: isEven ? -40 : 40 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={transition}
                    className="flex-1 flex flex-col justify-center"
                  >
                    <span className="text-xs font-semibold tracking-widest text-accent mb-4 block uppercase">
                      // Component {String(index + 1).padStart(2, "0")}
                    </span>
                    
                    <h3 className="text-2xl md:text-3xl font-header font-bold text-foreground mb-6">
                      {item.title}
                    </h3>
                    
                    <p className="text-base font-body font-light text-foreground/65 leading-relaxed mb-6">
                      {item.description}
                    </p>
                  </motion.div>

                  {/* Asymmetric Graphic Block */}
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true, margin: "-100px" }}
                    transition={transition}
                    className="flex-1 w-full relative min-h-[300px] md:min-h-[400px] rounded-custom overflow-hidden bg-cardBg border border-borderColor flex justify-center items-center shadow-custom"
                  >
                    {/* Visual artistic layering representing organic contrast */}
                    <div className="absolute inset-0 bg-gradient-to-tr from-accent/5 via-transparent to-muted/10" />
                    
                    {/* Floating luxury elements */}
                    <div className="relative w-40 h-40 md:w-56 md:h-56 rounded-custom border border-borderColor flex justify-center items-center">
                      <div className="w-24 h-24 rounded-custom border border-accent/20 border-dashed" />
                      {/* Bold rebel stroke across the elegant circle */}
                      <div className="absolute w-full h-[1px] bg-accent/20 rotate-45 transform" />
                    </div>

                    <div className="absolute top-6 left-6 font-mono text-[10px] tracking-wider text-muted select-none">
                      DNA_ONTOLOGY_LOCK: {item.title?.toUpperCase().substring(0, 10)}
                    </div>
                  </motion.div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}
