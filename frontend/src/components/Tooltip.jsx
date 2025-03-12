import * as React from 'react';
import { Tooltip } from '@base-ui-components/react/tooltip';

export default function TooltipPacker(prop) {
    return (
        <Tooltip.Provider>
            <Tooltip.Root>
                <Tooltip.Trigger aria-label="Bold">
                    <span>?</span>
                </Tooltip.Trigger>
                <Tooltip.Portal>
                    <Tooltip.Positioner sideOffset={10}>
                        <Tooltip.Popup>
                            <Tooltip.Arrow >
                                {/* <ArrowSvg /> */}
                            </Tooltip.Arrow>
                            Bold
                        </Tooltip.Popup>
                    </Tooltip.Positioner>
                </Tooltip.Portal>
            </Tooltip.Root>
        </Tooltip.Provider>
    );
}
